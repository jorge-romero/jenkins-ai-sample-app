pipeline {
    // Single agent for whole pipeline to guarantee same node + same workspace across stages.
    agent { label 'quality-tooling-agent' }

    environment {
        APP_DIR = '.'
        REPORTS_DIR = 'reports'
        BUILD_REMEDIATION_RETRIES = '3'
        GITHUB_TOKEN = credentials('github-token')
        GEMINI_API_KEY = credentials('gemini-api-key')
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout Shared Workspace') {
            steps {
                deleteDir()
                checkout scm
                dir("${APP_DIR}") {
                    sh 'mkdir -p ${REPORTS_DIR}'
                }
            }
        }

        stage('Build + Test + AI Remediation (Retry)') {
            steps {
                script {
                    int maxRetries = (env.BUILD_REMEDIATION_RETRIES ?: '3') as Integer
                    int attempt = 0

                    // Retry the whole block when exceptions occur.
                    // User aborts are not retried by Jenkins.
                    retry(
                        count: maxRetries,
                        conditions: [
                            agent(),
                            kubernetesAgent(handleNonKubernetes: true),
                            nonresumable()
                        ]
                    ) {
                        attempt += 1
                        echo "🔁 Build/remediation attempt ${attempt}/${maxRetries}"

                        dir("${APP_DIR}") {
                            sh '''
                                set -eu

                                # 1) Build/setup
                                python3 -m venv .venv
                                . .venv/bin/activate

                                python -m pip install --upgrade pip setuptools wheel
                                python -m pip install -r requirements.txt -r requirements-dev.txt

                                mkdir -p "${REPORTS_DIR}"
                                python -m pip list --format=json > "${REPORTS_DIR}/build-report.json"
                                python -m pip check > "${REPORTS_DIR}/pip-check.txt"

                                # First build/test verification (before remediation)
                                set +e
                                pytest -v \
                                  --junitxml="${REPORTS_DIR}/test-report.xml" \
                                  --cov=src \
                                  --cov-report=xml:"${REPORTS_DIR}/coverage.xml" \
                                  --cov-report=term-missing
                                INITIAL_PYTEST_EXIT=$?
                                set -e

                                if [ "$INITIAL_PYTEST_EXIT" -eq 0 ]; then
                                  echo "✅ Build/test passed. No remediation needed."
                                  exit 0
                                fi

                                if [ "$INITIAL_PYTEST_EXIT" -ne 1 ]; then
                                  echo "pytest failed with unexpected exit code before remediation: $INITIAL_PYTEST_EXIT"
                                  exit "$INITIAL_PYTEST_EXIT"
                                fi

                                # 2) Remediate only when needed
                                echo "🤖 Test failures detected. Running remediation..."

                                node /agent/unified-agent/dist/tooling/cli.js \
                                  --mode test \
                                  --technology python \
                                  --workspace "$(pwd)" \
                                  --report-input "${REPORTS_DIR}/test-report.xml" \
                                  --output "${REPORTS_DIR}/test-report.json"

                                test -f "${REPORTS_DIR}/test-report.json"

                                # Publication is intentionally disabled inside retry loop.
                                # PR will be created only after the retry stage finishes successfully.
                                NODE_ENV=test node /agent/unified-agent/dist/cli.js \
                                  --mode test \
                                  --report-file "${REPORTS_DIR}/test-report.json" \
                                  --output-file "${REPORTS_DIR}/test-remediation-result.json" \
                                  --workspace-dir "$(pwd)"

                                # 3) Build/test again to verify remediation impact
                                echo "🔁 Re-running build/test after remediation..."
                                set +e
                                pytest -v \
                                  --junitxml="${REPORTS_DIR}/test-report.after-remediation.xml" \
                                  --cov=src \
                                  --cov-report=xml:"${REPORTS_DIR}/coverage.after-remediation.xml" \
                                  --cov-report=term-missing
                                POST_REMEDIATION_EXIT=$?
                                set -e

                                if [ "$POST_REMEDIATION_EXIT" -eq 0 ]; then
                                  echo "✅ Build/test succeeded after remediation."
                                  exit 0
                                fi

                                if [ "$POST_REMEDIATION_EXIT" -ne 1 ]; then
                                  echo "pytest failed with unexpected exit code after remediation: $POST_REMEDIATION_EXIT"
                                  exit "$POST_REMEDIATION_EXIT"
                                fi

                                echo "❌ Tests still failing after remediation. Triggering Jenkins retry."
                                exit 1
                            '''
                        }
                    }
                }
            }
        }

        stage('Publish Test Remediation PR') {
            steps {
                echo '📬 Creating PR for test remediation changes (after retry block)...'
                dir("${APP_DIR}") {
                    sh '''
                        set -eu

                        if [ ! -f "${REPORTS_DIR}/test-remediation-result.json" ]; then
                          echo "No remediation result found. Skipping PR publication."
                          exit 0
                        fi

                        APPLIED_FILES_COUNT=$(python - <<'PY'
import json
from pathlib import Path

result_file = Path('reports/test-remediation-result.json')
try:
    payload = json.loads(result_file.read_text(encoding='utf-8'))
except Exception:
    print(0)
else:
    files = payload.get('appliedFiles') if isinstance(payload, dict) else []
    print(len(files) if isinstance(files, list) else 0)
PY
                        )

                        if [ "${APPLIED_FILES_COUNT}" -eq 0 ]; then
                          echo "Remediation did not apply files. Skipping PR publication."
                          exit 0
                        fi

                        node --input-type=module <<'NODE'
import fs from 'node:fs';
import path from 'node:path';
import { publishRemediationToGitHub } from '/agent/unified-agent/dist/remediation/github-publication.js';

const workspaceDir = process.cwd();
const reportsDir = path.join(workspaceDir, 'reports');
const remediationResultPath = path.join(reportsDir, 'test-remediation-result.json');
const publicationOutputPath = path.join(reportsDir, 'test-remediation-publication.json');

const remediation = JSON.parse(fs.readFileSync(remediationResultPath, 'utf8'));
const appliedFiles = Array.isArray(remediation.appliedFiles) ? remediation.appliedFiles : [];

if (appliedFiles.length === 0) {
  const skipped = {
    attempted: false,
    status: 'skipped',
    reason: 'No files were applied by remediation; skipping commit and PR.',
  };
  fs.writeFileSync(publicationOutputPath, JSON.stringify(skipped, null, 2));
  console.log(JSON.stringify(skipped));
  process.exit(0);
}

const config = {
  workspaceDir,
  github: {
    token: process.env.GITHUB_TOKEN,
    username: process.env.GITHUB_USERNAME,
    repository: process.env.GITHUB_REPO ?? 'jenkins-ai-sample-app',
  },
};

const publication = await publishRemediationToGitHub({
  config,
  mode: 'test',
  providerName: remediation.provider ?? 'unknown',
  summary: remediation.summary ?? 'Automated test remediation',
  reportFile: path.join('reports', 'test-report.json'),
  appliedFiles,
});

fs.writeFileSync(publicationOutputPath, JSON.stringify(publication, null, 2));
console.log(JSON.stringify(publication));

if (publication.status === 'failed') {
  process.exit(1);
}
NODE
                    '''
                }
            }
        }

        stage('Python Vulnerability/Quality Scan + Report') {
            steps {
                echo '🔍 Running vulnerability/quality scan and generating report...'
                dir("${APP_DIR}") {
                    sh '''
                        set -eu

                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip setuptools wheel
                        python -m pip install -r requirements.txt -r requirements-dev.txt

                        mkdir -p "${REPORTS_DIR}"

                        node /agent/unified-agent/dist/tooling/cli.js \
                            --mode quality \
                            --technology python \
                            --workspace "$(pwd)" \
                            --output "${REPORTS_DIR}/quality-report.json"
                    '''
                }
            }
        }

        stage('Smart Check Vulnerability Report + Remediate') {
            steps {
                echo '🤖 Checking vulnerability/quality report and remediating when thresholds are breached...'
                dir("${APP_DIR}") {
                    sh '''
                        set -e
                        test -f "${REPORTS_DIR}/quality-report.json"

                        node /agent/unified-agent/dist/cli.js \
                            --mode quality \
                            --report-file "${REPORTS_DIR}/quality-report.json" \
                            --output-file "${REPORTS_DIR}/quality-remediation-result.json" \
                            --workspace-dir "$(pwd)"
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo '🚀 Deploying application...'
                echo 'Deployment would happen here in production'
            }
        }
    }

    post {
        always {
            echo '=' * 80
            echo 'Pipeline completed'
            echo '=' * 80
            dir("${APP_DIR}") {
                stash name: 'reports-files', includes: "${REPORTS_DIR}/**/*", allowEmpty: true
            }
            archiveArtifacts artifacts: "${REPORTS_DIR}/*.json,${REPORTS_DIR}/*.xml,${REPORTS_DIR}/*.txt", allowEmptyArchive: true
        }
        success {
            echo '✅ All stages completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed'
            echo 'Check logs for details'
        }
        unstable {
            echo '⚠️  Pipeline unstable - review remediation reports in artifacts'
        }
    }
}

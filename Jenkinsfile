pipeline {
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
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
                dir("${APP_DIR}") { sh 'mkdir -p ${REPORTS_DIR}' }
            }
        }
        stage('Setup environment') {
            steps {
                dir("${APP_DIR}") {
                    sh '''
                    set -e
                    mkdir -p "${REPORTS_DIR}"
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                                         pip install -r requirements-dev.txt
                     '''
                 }
             }
        }

        stage('Test → Remediate → Verify') {
            steps {
                    script {
                    int maxRetries = (env.BUILD_REMEDIATION_RETRIES ?: '3').toInteger()

                    retry(maxRetries) {
                        dir("${APP_DIR}") {
                        // Determinar número de intento (retry no expone contador, lo calculamos con un archivo temporal)
                        int attempt = sh(script: 'echo $(( $(cat .attempt 2>/dev/null || echo 0) + 1 )) | tee .attempt', returnStdout: true).trim().toInteger()

                        int testExit = sh(
                            script: """
                            set +e
                            . .venv/bin/activate
                            pytest -v --junitxml="${REPORTS_DIR}/test-report-attempt-${attempt}.xml" \
                                --cov=src --cov-report=xml:"${REPORTS_DIR}/coverage-attempt-${attempt}.xml"
                            exit \$?
                            """,
                            returnStatus: true
                        )

                        echo "Test exit code: ${testExit}"

                        if (testExit == 0) {
                            echo "Tests OK en intento ${attempt}. No remediation needed."
                            sh 'rm -f .attempt' // limpiar contador
                            return
                        }

                        // Remediación
                        sh(
                            script: """
                            node /agent/unified-agent/dist/tooling/cli.js --mode test --technology python \
                            --workspace "$(pwd)" --report-input "${REPORTS_DIR}/test-report-attempt-${attempt}.xml" \
                            --output "${REPORTS_DIR}/test-report-attempt-${attempt}.json"

                            NODE_ENV=test node /agent/unified-agent/dist/cli.js --mode test \
                            --report-file "${REPORTS_DIR}/test-report-attempt-${attempt}.json" \
                            --output-file "${REPORTS_DIR}/test-remediation-result-attempt-${attempt}.json" \
                            --workspace-dir "$(pwd)"
                            """
                        )

                        // Forzar fallo para que retry() repita
                        error "Intento ${attempt} fallido"
                        }
                    }
                }
            }
        }

         stage('Quality → Remediate → Verify') {
                steps {
                script {
                    retry(
                        count: (env.BUILD_REMEDIATION_RETRIES ?: '3') as Integer,
                        conditions: [agent(), nonresumable()]
                    ) {
                        dir("${APP_DIR}") {
                            sh '''
                                set -eu
                                python3 -m venv .venv && . .venv/bin/activate
                                python -m pip install -q --upgrade pip setuptools wheel
                                python -m pip install -q -r requirements.txt -r requirements-dev.txt

                                node /agent/unified-agent/dist/tooling/cli.js --mode quality --technology python \
                                    --workspace "$(pwd)" --output "${REPORTS_DIR}/quality-report.json"

                                if node /agent/unified-agent/dist/cli.js --mode quality \
                                    --report-file "${REPORTS_DIR}/quality-report.json" \
                                    --output-file "${REPORTS_DIR}/quality-remediation-result.json" \
                                    --workspace-dir "$(pwd)"; then exit 0; fi

                                node /agent/unified-agent/dist/tooling/cli.js --mode quality --technology python \
                                    --workspace "$(pwd)" --output "${REPORTS_DIR}/quality-report.json"

                                node /agent/unified-agent/dist/cli.js --mode quality \
                                    --report-file "${REPORTS_DIR}/quality-report.json" \
                                    --output-file "${REPORTS_DIR}/quality-remediation-result.json" \
                                    --workspace-dir "$(pwd)" && exit 0

                                exit 1
                            '''
                        }
                    }
                }
            }
        }

        stage('Publish Remediation') {
            steps {
                dir("${APP_DIR}") {
                    sh '''
                        set -eu
                        [ ! -f "${REPORTS_DIR}/test-remediation-result.json" ] && exit 0
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
  fs.writeFileSync(publicationOutputPath, JSON.stringify({attempted:false,status:'skipped'}));
  process.exit(0);
}
const publication = await publishRemediationToGitHub({
  config: { workspaceDir, github: { token: process.env.GITHUB_TOKEN, username: process.env.GITHUB_USERNAME, repository: process.env.GITHUB_REPO ?? 'jenkins-ai-sample-app' } },
  mode: 'test', providerName: remediation.provider ?? 'unknown', summary: remediation.summary ?? 'Automated test remediation',
  reportFile: 'reports/test-report.json', appliedFiles,
});
fs.writeFileSync(publicationOutputPath, JSON.stringify(publication));
if (publication.status === 'failed') process.exit(1);
NODE
                    '''
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps { echo 'Deploying application...' }
        }
    }

    post {
        always {
            dir("${APP_DIR}") { stash name: 'reports-files', includes: "${REPORTS_DIR}/**/*", allowEmpty: true }
            archiveArtifacts artifacts: "${REPORTS_DIR}/*.json,${REPORTS_DIR}/*.xml,${REPORTS_DIR}/*.txt", allowEmptyArchive: true
        }
        success { echo '✅ Pipeline succeeded' }
        failure { echo '❌ Pipeline failed' }
        unstable { echo '⚠️  Pipeline unstable' }
    }
}

pipeline {
    // Single agent for whole pipeline to guarantee same node + same workspace across stages.
    agent { label 'quality-tooling-agent' }

        environment {
        APP_DIR = '.'
        REPORTS_DIR = 'reports'
        GITHUB_TOKEN = credentials('github-token')
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

        stage('Python Build + Test + Build Report') {
            steps {
                echo '🔨 Running Python build/dependency install and generating build report...'
                dir("${APP_DIR}") {
                    sh '''
                        set -eu

                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip setuptools wheel
                        python -m pip install -r requirements.txt -r requirements-dev.txt

                        mkdir -p "${REPORTS_DIR}"

                        # Build report (standard Python metadata + dependency health)
                        python -m pip list --format=json > "${REPORTS_DIR}/build-report.json"
                        python -m pip check > "${REPORTS_DIR}/pip-check.txt"

                        # Test reports (standard pytest outputs)
                        # Allow exit code 1 (test failures) so remediation stage can run.
                        set +e
                        pytest -v \
                          --junitxml="${REPORTS_DIR}/test-report.xml" \
                          --cov=src \
                          --cov-report=xml:"${REPORTS_DIR}/coverage.xml" \
                          --cov-report=term-missing
                        PYTEST_EXIT=$?
                        set -e

                        if [ "$PYTEST_EXIT" -ne 0 ] && [ "$PYTEST_EXIT" -ne 1 ]; then
                          echo "pytest failed with unexpected exit code: $PYTEST_EXIT"
                          exit "$PYTEST_EXIT"
                        fi
                    '''
                }
            }
        }

                stage('Smart Check Test Report + Remediate') {
            steps {
                echo '🤖 Checking test report and remediating when failures are detected...'
                dir("${APP_DIR}") {
                    sh '''
                        set -e
                        test -f "${REPORTS_DIR}/test-report.xml"

                        # Convert JUnit XML to normalized test-report.json expected by remediation runtime
                        node /agent/unified-agent/dist/tooling/cli.js \
                            --mode test \
                            --technology python \
                            --workspace "$(pwd)" \
                            --report-input "${REPORTS_DIR}/test-report.xml" \
                            --output "${REPORTS_DIR}/test-report.json"

                        test -f "${REPORTS_DIR}/test-report.json"

                        node /agent/unified-agent/dist/cli.js \
                            --mode test \
                            --report-file "${REPORTS_DIR}/test-report.json" \
                            --output-file "${REPORTS_DIR}/test-remediation-result.json" \
                            --workspace-dir "$(pwd)"
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

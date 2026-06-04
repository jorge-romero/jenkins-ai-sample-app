pipeline {
    agent none

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Checkout') {
            agent { label 'build-agent' }
            steps {
                echo '📦 Checking out code...'
                checkout scm
            }
        }

        stage('Build') {
            agent { label 'build-agent' }
            steps {
                echo '🔨 Installing dependencies...'
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            agent { label 'test-ai-agent' }
            steps {
                echo '🧪 Running tests with AI-powered fixing...'
                script {
                    // AI agent runs tests, detects failures,
                    // analyzes with Gemini, applies fixes, and creates PR
                    sh '''
                        # Each stage runs in a different Jenkins agent container.
                        # Install app dependencies here so pytest can import FastAPI modules.
                        python3 -m pip install --upgrade pip
                        python3 -m pip install -r requirements.txt -r requirements-dev.txt

                        export WORKSPACE=$(pwd)
                        python3 /agent/ai_test_fixer.py || true
                    '''
                }
            }
        }

        stage('Quality Analysis') {
            agent { label 'quality-ai-agent' }
            steps {
                echo '📊 Running quality analysis with AI-powered fixing...'
                script {
                    // AI agent runs ruff & bandit, detects issues,
                    // analyzes with Gemini, applies fixes, and creates PR
                    sh '''
                        # Each stage runs in a different Jenkins agent container.
                        # Install app + tooling deps required by quality analysis.
                        python3 -m pip install --upgrade pip
                        python3 -m pip install -r requirements.txt -r requirements-dev.txt

                        export WORKSPACE=$(pwd)
                        python3 /agent/ai_quality_fixer.py || true
                    '''
                }
            }
        }

        stage('Deploy') {
            agent { label 'build-agent' }
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
        }
        success {
            echo '✅ All stages completed successfully!'
            echo 'Check GitHub for AI-generated PRs with fixes.'
        }
        failure {
            echo '❌ Pipeline failed'
            echo 'Check logs for details'
        }
        unstable {
            echo '⚠️  Pipeline unstable - AI agents may have created PRs'
            echo 'Review and merge the PRs to fix issues'
        }
    }
}

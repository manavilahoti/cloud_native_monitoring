pipeline {
  agent any

  environment {
    SONAR_HOST_URL = 'http://localhost:9000'
    SONAR_TOKEN    = credentials('sonar-token')
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/manavilahoti/cloud_native_monitoring', branch: 'feature/pipeline'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        sh '''
          # ensure sonar-scanner is on the PATH
          export PATH="/usr/local/sonar-scanner/bin:$PATH"

          # run the analysis
          sonar-scanner \
            -Dsonar.host.url=${SONAR_HOST_URL} \
            -Dsonar.login=${SONAR_TOKEN}
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker build \
            --platform linux/amd64 \
            -t 779846818072.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-native-repo:latest \
            .
        '''
      }
    }

    stage('Push to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region ap-south-1 \
            | docker login --username AWS --password-stdin 779846818072.dkr.ecr.ap-south-1.amazonaws.com

          docker push 779846818072.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-native-repo:latest
        '''
      }
    }

    stage('Deploy to EKS') {
      steps {
        sh 'kubectl apply -f deployment.yaml'
        sh 'kubectl apply -f service.yaml'
      }
    }
  }

  post {
    always {
      echo "Pipeline finished with status: ${currentBuild.currentResult}"
    }
  }
}

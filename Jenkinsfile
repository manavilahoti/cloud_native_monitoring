pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/manavilahoti/cloud_native_monitoring', branch: 'feature/pipeline'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                sh '''
                export PATH="/usr/local/sonar-scanner/bin:$PATH"
                sonar-scanner
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build --platform linux/amd64 -t 779846818072.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-native-repo:latest .'
            }
        }
        stage('Push to ECR') {
            steps {
                sh 'aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 779846818072.dkr.ecr.ap-south-1.amazonaws.com'
                sh 'docker push 779846818072.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-native-repo:latest'
            }
        }
        stage('Push to Artifactory') {
            steps {
                sh 'docker tag 779846818072.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-native-repo:latest localhost:8081/docker-local/my-cloud-native-repo:latest'
                sh 'docker login -u admin -p yourpassword localhost:8081'
                sh 'docker push localhost:8081/docker-local/my-cloud-native-repo:latest'
            }
        }
        stage('Deploy to EKS') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
}

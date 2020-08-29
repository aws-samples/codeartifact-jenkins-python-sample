// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

pipeline {
  agent any
  environment {
    AWS_ACCOUNT_ID = 'Your AWS Account ID'
    AWS_REGION = 'Region you used for this project'
    AWS_CA_DOMAIN = 'Name of your CodeArtifact domain'
    AWS_CA_REPO = 'Name of your CodeArtifact repository'
    AWS_STACK_NAME = 'Name of the CloudFormation stack'
    CONTAINER_NAME = 'Container name provided to CloudFormation'
    CREDENTIALS_ID = 'Jenkins credentials ID' 
  }
  stages {

    stage('Pre-Build') {
      steps {
        sh "aws configure set region ${AWS_REGION}"
        sh "aws --version"
        sh "docker version"
      }
    }

    stage('Create Docker Image') {
      steps {
        script {
          //Retrieve the CodeArtifact authenthication token
          withCredentials([usernamePassword(
            credentialsId: CREDENTIALS_ID,
            passwordVariable: 'AWS_SECRET_ACCESS_KEY',
            usernameVariable: 'AWS_ACCESS_KEY_ID'
          )]) {
            authToken = sh(
              returnStdout: true,
              script: 'aws codeartifact get-authorization-token \
              --domain $AWS_CA_DOMAIN \
              --query authorizationToken \
              --output text \
              --duration-seconds 900'
            ).trim()

          }

          //Pass the CodeArtifact token as an argument to Docker build
          //Using docker build command directly intead of the docker.build() function to conceal the token from logs
          echo "Running docker build..."
          sh ("""
            set +x
            docker build -t $CONTAINER_NAME:$BUILD_NUMBER \
            --build-arg CODEARTIFACT_TOKEN='$authToken' \
            --build-arg DOMAIN=$AWS_CA_DOMAIN-$AWS_ACCOUNT_ID \
            --build-arg REGION=$AWS_REGION \
            --build-arg REPO=$AWS_CA_REPO .
          """)

        }

      }
    }

    stage('Test') {
      steps {
        script {
          //Start a docker container based on the image and make sure it responds to HTTP requests
          docker.image('$CONTAINER_NAME:$BUILD_NUMBER').withRun('-p 5000:8080') { c ->
            sh 'sleep 5'
            sh 'curl http://127.0.0.1:5000/ --verbose'
          }
        }
      }
    }

    stage('Publish to ECR') {
      steps {
        script {
          withCredentials([usernamePassword(
            credentialsId: CREDENTIALS_ID,
            passwordVariable: 'AWS_SECRET_ACCESS_KEY',
            usernameVariable: 'AWS_ACCESS_KEY_ID')]) {

              docker.withRegistry('https://${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com') {
                //Retrieve the Amazon ECR authenthication token, and use it to configure the Docker daemon
                sh """
                  aws ecr get-login-password \
                  | docker login \
                  --username AWS \
                  --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                  """

                  //Push image to ECR
                  docker.image("$CONTAINER_NAME:$BUILD_ID").push()
              }
          }
        }
      }
    }

    stage('Deploy to ECS') {
      steps {
        script {
          //Update CloudFormation template with the new image tag. This will cause CloudFormation to start a new deployment to ECS
          withCredentials([usernamePassword(
            credentialsId: CREDENTIALS_ID,
            passwordVariable: 'AWS_SECRET_ACCESS_KEY',
            usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
              sh "aws cloudformation deploy \
              --stack-name $AWS_STACK_NAME \
              --template-file application.yml \
              --parameter-overrides ImageTag=$BUILD_ID \
              --capabilities CAPABILITY_NAMED_IAM"
          }
        }
      }
    }
  }
}

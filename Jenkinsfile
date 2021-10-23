pipeline {
    agent any
    environment {
            docker_user = 'richie31'
            registryCredential = 'dockerhub'
            project_name = "api"
            semi_colon = ':'
            slash = '/'
            ver = "latest"
    }

    stages {
        stage("Checkout"){

            
            steps{
            checkout([$class: 'GitSCM', branches: [[name: 'master']], extensions: [], userRemoteConfigs: [[credentialsId: '621b2d88-0c28-4ce2-93e3-997889f14448', url: 'https://github.com/richie312/CommonDatabaseAPI.git']]])
            sh "echo $params.current_status"
            sh "echo $params.merged"
            sh "echo $params.branch"

             }
        }


        stage('BuildPreparations')
        {
            when {
                  expression { return params.branch == "master" && params.current_status == "closed" && params.merged == "closed" }
              }
            steps
            {
                script
                {
                    // calculate GIT lastest commit short-hash
                    gitCommitHash = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    shortCommitHash = gitCommitHash.take(7)
                    // calculate a sample version tag
                    VERSION = shortCommitHash
                    // set the build display name
                    currentBuild.displayName = "#${BUILD_ID}-${VERSION}"
                    IMAGE = "$project_name:$ver"
                    println "${params.current_status}"
                }
            }
        }

        stage('BuildStage'){
            when {
                  expression { return params.branch == "master" && params.current_status == "closed" && params.merged == "closed" }
              }

            steps {
                    script {
                        sh  "docker login -u $env.docker_user -p Kevalasya@123"
                        sh  "docker build -t $docker_user$slash$IMAGE ."
                    }
                // timeout(10){}
                // script{
                //     echo "The container is active and application is live @ localhost:5001"
                //     }
                }
            }

        stage('PostBuild'){

            when {
                  expression { return params.branch == "Master" && params.current_status == "closed" && params.merged == "closed" }
              }

            steps {
                    script {
                       sh " docker push $docker_user$slash$IMAGE"
                       sh "echo docker image has been pushed to the docker repository."
                       sh "docker rmi $docker_user$slash$IMAGE"
                       sh "docker rmi python:latest"
                       sh "echo removed the base python image as well."
                    }
                }
            }
        
    
        stage('Deployment'){

            when {
                  expression { return params.branch == "master" && params.current_status == "closed" && params.merged == "closed" }
              }

            steps {
                    script {
                       sh " echo stopping and removing the previous build container..."
                       sh "docker rm --force api_container"
                       sh "echo removing old image..."
                       sh "docker rmi $docker_user$slash$IMAGE"
                       sh "echo pull updated image ..."
                       sh "docker pull $docker_user$slash$IMAGE"
                       sh "echo running the image ..."
                       sh "docker run --memory=512m --name api_container -p 5001:5001 $docker_user$slash$IMAGE:latest"
                    }
                }
            }
        }

    }
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
            checkout([$class: 'GitSCM', branches: [[name: 'Develop']], extensions: [], userRemoteConfigs: [[credentialsId: '621b2d88-0c28-4ce2-93e3-997889f14448', url: 'https://github.com/richie312/CommonDatabaseAPI.git']]])
             }
        }


        stage('Build preparations')
        {
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
                }
            }
        }

        stage('build_stage'){
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

        stage('post_build'){
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
        
        }
    

    }
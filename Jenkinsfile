pipeline {
    agent {
        kubernetes {
            label 'history-python-builder'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - sleep
    args:
    - 9999999
    volumeMounts:
    - name: kaniko-secret
      mountPath: /kaniko/.docker
  - name: kubectl
    image: alpine/k8s:1.29.11
    command:
    - sleep
    args:
    - 9999999
  volumes:
  - name: kaniko-secret
    secret:
      secretName: regcred
"""
        }
    }

    stages {
        stage('Checkout') {
            steps {
                container('kaniko') {
                    checkout scm
                    sh """ ls """
                }
            }
        }

        stage('Build and Push Image') {
            steps {
                container('kaniko') {
                    script {
                        // 使用 Kaniko 构建并推送，打两个 tag：构建号 和 latest
                        sh """
                            /kaniko/executor --context=dir://${WORKSPACE} \
                              --destination=crpi-ylw7gpcmxpqjz8c6.cn-wulanchabu.personal.cr.aliyuncs.com/myvote/history:${BUILD_NUMBER} \
                              --destination=crpi-ylw7gpcmxpqjz8c6.cn-wulanchabu.personal.cr.aliyuncs.com/myvote/history:latest \
                              --cache=true \
                              --verbosity=debug \
                              --cache-repo=crpi-ylw7gpcmxpqjz8c6.cn-wulanchabu.personal.cr.aliyuncs.com/myvote/history-cache
                        """
                    }
                }
            }
        }

        stage('Update K8s Deployment') {
            steps {
                container('kubectl') {
                    script {
                        // 更新 deployment 镜像版本
                        sh """
                            sed -i "s|image: .*|image: crpi-ylw7gpcmxpqjz8c6.cn-wulanchabu.personal.cr.aliyuncs.com/myvote/history:${BUILD_NUMBER}|g" history-service.yaml
                            kubectl apply -f history-service.yaml
                            kubectl rollout status deployment/history-service -n sock-shop
                            ls
                        """
                    }
                }
            }
        }
    }
}

export META_UPSTREAM_DIR="git@github.com:Project-Tick/meta-upstream.git"
export META_LAUNCHER_DIR="git@github.com:Project-Tick/meta-launcher.git"
export DEPLOY_TO_FOLDER=false
export DEPLOY_FOLDER=/app/public/v1
export DEPLOY_FOLDER_USER=http
export DEPLOY_FOLDER_GROUP=http

export DEPLOY_TO_GIT=true
export GIT_AUTHOR_NAME="YONG Do Hyun"
export GIT_AUTHOR_EMAIL="froster12@naver.com"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
export GIT_SSH_COMMAND="ssh -i ${BASEDIR}/config/deploy.key"

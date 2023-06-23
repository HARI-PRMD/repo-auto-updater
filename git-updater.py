import subprocess
from flask import Flask, request
from git import Repo

# Path to your local repository
REPO_PATH = "/path/to/your/local/repository"

# Branch to pull changes from
BRANCH = "main"

# Server command to restart
SERVER_COMMAND = "npm run build && npm run start"

# Initialize the repository object
repo = Repo(REPO_PATH)

# Flask application
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-GitHub-Event') == 'push':
        payload = request.get_json()
        ref = payload['ref']

        if ref.endswith(BRANCH):
            print(f"Webhook received. Pulling changes from {BRANCH} branch...")
            repo.git.pull("origin", BRANCH)

            print("Restarting server...")
            subprocess.call(SERVER_COMMAND, shell=True)

            return 'Pull and server restart successful', 200

    return 'No action taken', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

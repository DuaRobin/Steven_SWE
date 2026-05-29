import subprocess


def get_identity_token():
    try:
        # This literally runs `gcloud auth print-identity-token` behind the scenes
        token = subprocess.check_output(
            ["gcloud", "auth", "print-identity-token"], text=True
        ).strip()
        return token
    except subprocess.CalledProcessError:
        raise RuntimeError("gcloud command failed. Are you logged in on your terminal?")


if __name__ == "__main__":
    print(get_identity_token())
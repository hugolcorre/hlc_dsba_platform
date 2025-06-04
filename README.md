
# DSBA Platform – Installation Guide

This guide explains how to properly set up and run the project in a local development environment.

---

## 1. Download the Project

### Option A – Clone via Git

```bash
cd ~/Desktop
git clone https://github.com/your-username/hlc_dsba_platform.git dsba-platform
```

> Note: The folder is renamed to `dsba-platform` for consistency with environment paths.

### Option B – Download ZIP

1. Go to the GitHub repository.
2. Click **“Code”** > **“Download ZIP”**.
3. Extract the ZIP to `~/Desktop` and rename the folder to `dsba-platform`.

---

## 2. Open the Project in VS Code

* Launch Visual Studio Code.
* Open the `~/Desktop/dsba-platform` folder.
* Open a terminal using: `Ctrl + Shift + ` (backtick key).

---

## 3. Set Up the Virtual Environment

In the terminal, run:

```bash
pip install hatch
hatch env create
hatch shell
pip install -e .
```

---

## 4. Set Environment Variables

Add the following lines to the end of your `~/.zshrc` (or `~/.bashrc` if using Bash):

```bash
echo 'export PYTHONPATH="$PYTHONPATH:$HOME/Desktop/dsba-platform/src"' >> ~/.zshrc
echo 'export DSBA_MODELS_ROOT_PATH="$HOME/Desktop/dsba-platform/models"' >> ~/.zshrc
```

Then apply the changes:

```bash
source ~/.zshrc
```

---

## 5. Verify the Setup

In your terminal (inside the project directory), run:

```bash
hatch shell
./src/cli/dsba_cli list
```

This should print a list of available models. If none exist yet, you'll see a message indicating that.

---

## 6. (Optional) Run the API with Docker

### Build the Docker image

```bash
./src/cli/dsba_cli build_image
```

### Run the Docker container

```bash
./src/cli/dsba_cli run_container
```

Once running, the API will be accessible at:

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 7. User Guide

A **User Guide** is included in the repository to help you understand and use the available CLI commands.

> It explains how to preprocess data, train models, list models, make predictions, and more using `./src/cli/dsba_cli`.

Refer to this document to navigate the platform's functionalities from the terminal.


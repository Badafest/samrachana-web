### Content <!-- omit in toc -->

- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [For Developers](#for-developers)
- [Frequently Asked Questions](#frequently-asked-questions)

---

### Introduction

Samrachana is a free and open source structural analysis software based on Direct Stiffness Method. It is ideal for analysing 2D beams, frames and trusses.

> If you find a bug or an issue, kindly post it in the [discussion forum](https://github.com/badafest/samrachana-web/discussions)

---

| [Go To Tutorials](https://github.com/Badafest/samrachana-web/wiki) | [See Releases](https://github.com/Badafest/samrachana-web/releases) | [See Issues](https://github.com/Badafest/samrachana-web/issues) |
| ------------------------------------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------- |

---

### Installation

1.  ##### Windows

    > Although you can install Samrachana as an executable application, I don't recommend that right now.

    To install Samrachana on Windows, you can download installer from [here](https://github.com/Badafest/samrachana-web/releases/download/v1.0.0/samrachana-1.0.0.Setup.exe) and simply run it. After the installation is completed, you can launch Samrachana just like you launch any other software.

    > To avoid fetching the executable time and again, **Pin to Taskbar** during the first run.

    > Samrachana is installed in `~/AppData/Local/samrachana` by default. To uninsall it, run this command on your terminal:

    ```
    remove-item ~/AppData/Local/samrachana
    ```

2.  ##### MacOS, Linux or other OS [^1]

    [^1]: Installers for these systems will be available soon.

    At the moment, no installer is available for operration systems other than windows. So, the only option is to [setup development](#setup-development).

3.  ##### Setup Development [^2]

    [^2]: If you want to contribute, please refer [For Developers](#for-developers) section.

    If you just want to try out Samrachana, or want to contribute to this repository, the best way to install it is this way. You can follow these steps to setup development environment:

    1.  Install `Python3.8.5` in your computer. [Official Downloads](https://www.python.org/ftp/python/3.8.5)
    2.  Install `Node 18` in your computer. [Official Downloads](https://nodejs.org/dist/v18.13.0)
    3.  Clone the repository by typing this in your terminal:  
         `git clone https://github.com/badafest/samrachana-web.git`

        Or, click the button looking like:  
         ![clone button](./.github/img/code.png)  
         on top right.

    4.  Create a virtual environmant and run `activate` by typing these on your terminal(Optional).  
        Replace `directory-of-cloned-repo` by the actual directory in which the repo is cloned. It is `samrachana-web` by default.  
        The second line creates virtual environment in a hidden folder titled `.venv` inside the directory.  
        [(You can find the details Here)](https://docs.python.org/3/library/venv.html)  
        The last line activates virtual environment so that the dependencies are not installed globally.

        ```
        cd ./directory-of-cloned-repo/server
        python3 -m venv ./.venv
        .venv/Scripts/activate
        ```

    5.  Install the dependencies [`numba`]:

        ```
        pip3 install -r ./src/python/requirements.txt
        ```

    6.  Install `node_modules`:

        ```
        npm install
        ```

    7.  Make `.env` file from `.env.example` and run the server: [For general user, the commented values should work just fine]

        ```
        npm run dev
        ```

    8.  To setup frontend, first `cd` to `frontend`, install the package by `npm install` and then make `.env` file from `.env.example`. Then run the development server:

        ```
        npm run dev
        ```

        You can then use the address shown in terminal to open samrachana on broswer.

---

### Getting Started

Samrachana is made keeping users interested in function rather than interface of the application in mind. So, the learning curve of interface is as straight as possible. The basic keyboard shortcuts are shown in the right sidebar when there is no other form to show.
For detail documentation of all the features available, refer to the docs [here](https://github.com/Badafest/samrachana-web/wiki).

---

### For Developers

If you are interested in contributing to this repository and make Samrachana a better software, you can start by reading the [CONTRIBUTING markdown file](./CONTRIBUTING.md).

If you are intereseted in contributing [write me a mail](mailto:er.sandipdahal@gmail.com).

---

### Frequently Asked Questions

> Before asking questions in discussion forum, please make sure that your question is not already answered in this document.

1. Is Samrachana free to use?

   Samrachana is and always will be open source and free. You can not only use the software for free, but also download and modify the source code too. For details regarding what you can and can't do with the software and the source code, please read the [LICENSE file](LICENSE).

2. How can I install Samrachana in my phone?

   Samrachana is a desktop application and can't be installed in other devices. (Or at least, it is not intended to be.)

3. Can I work with 3D structures in Samrachana?

   Unfortunately, you can't work with 3D structures currently. However, we are working to develop a 3D version of the software too.

4. Can Samrachana perform Finite Element Analysis?

   In general, no. Samrachana is entirely designed for students just getting familiar with structural analysis. So, it only supports one dimensional line elements. (Although, curves are supported, they are broken down into small lines behind the scenes.) One can argue that, FEA can be performed to some extent using the software, but we will develop a separate version for that. So, stay tuned.

5. Can I submit my assignments using Samrachana?

   Note that, the software comes with absolutely no warranty or liability. If your professor and institution has no problem with using the software to complete your assingments, that is completely fine with us. However, you can always use it to check your answers!

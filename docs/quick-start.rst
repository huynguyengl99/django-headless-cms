=============
Quick Start
=============

Why is this section placed first? Because a small demo is worth a thousand times more than raw documentation. This demo uses Django-Headless-CMS to create content and publish APIs while utilizing Astrowind as the front-end framework for display.

What This Demo Includes
=======================

A. Backend - Django-Headless-CMS
--------------------------------
- Multi-language content support.
- Auto-generated API documentation & playground.
- Publish/Draft version management for content.
- Reversible content.
- Import/Export content.
- Sortable items.
- Markdown editor & preview.
- Custom admin interface: custom language for the admin panel, custom themes.
- API for Astrowind content.

B. Frontend - Astrowind
-----------------------
- Multi-language UI.
- Language switch button.
- Dynamic slugs for different post pages/tags.

Additional Note
===============

If you encounter any issues or errors while following this tutorial, please check the issues section or create a new one.

Prerequisites
=============

- Python >= 3.9 (you can use `PyENV <https://github.com/pyenv/pyenv>`_ to easily install and manage your Python versions).
- Cookiecutter installed. Refer to the `Cookiecutter documentation <https://cookiecutter.readthedocs.io/en/stable/README.html#installation>`_ for installation instructions.
- NVM installed (required for using Astrowind). Refer to `NVM GitHub <https://github.com/nvm-sh/nvm>`_ for installation instructions, or alternatively, install Node.js >= 18.

Getting Started
===============

a) Create a Workspace for Both Backend and Frontend
---------------------------------------------------

First, create a folder to contain both the backend (BE) and frontend (FE) projects:

.. code-block:: shell

    mkdir "/path/to/parent"
    cd "/path/to/parent"

b) Backend - Django-Headless-CMS Setup
--------------------------------------

Make sure you have installed `cookiecutter` as mentioned above, then run this command to bootstrap our backend with an opinionated template. **Note:** Select option **2** - `AstroWind` template at step 10:

.. code-block:: shell

    python -m cookiecutter https://github.com/huynguyengl99/cookiecutter-djhcms

.. image:: images/quick-start/cookiecutter.png
   :alt: DjHCMS Cookiecutter

- Open the created project.
- Follow the `README.md` inside the created project to initialize the backend, up to and including section `4. Getting Started`.
- After completing the setup, check the API.
- Visit http://localhost:8000/api/cms-schema/swg/ in incognito mode (to use the language code in the API header, otherwise it will be overridden by the Django admin language session). Input the generated API key in `Authorize`. (If you forget this step, refer to the BE `README.md`, which starts with `In order to use the below API playground, create an API key`).
- Example:

.. image:: images/quick-start/index_request.png
   :alt: Index request

You should receive a response like this:

.. image:: images/quick-start/index_response.png
   :alt: Index response

If you see the request and response as shown above, the backend setup is complete. Let's move to the next part.

c) Frontend - Django Astrowind Setup
------------------------------------

- Change the directory back to the parent workspace.
- Clone the GitHub repository (you can rename it if you want):

.. code-block:: shell

    git clone https://github.com/huynguyengl99/django-astrowind.git

- Open the cloned project.
- Copy `.env.TEMPLATE` to `.env` and add the generated API key to the environment variables.
- Install dependencies:

.. code-block:: shell

    npm install

- Run the project:

.. code-block:: shell

    npm run dev

- [Optional] When you want to deploy the site, modify the `src/config.yml` file.
- If everything works well, you should see the page open, navigate between tabs, and change languages, even for posts.

Examples:
- Home page in `English`:

.. image:: images/quick-start/home-page.png
   :alt: Home page

- Pricing page in `Chinese`:

.. image:: images/quick-start/zh-pricing.png
   :alt: Pricing page

- Post list page in `Vietnamese`:

.. image:: images/quick-start/vn-post-list.png
   :alt: Post list

- Post article page in `Arabic`:

.. image:: images/quick-start/ar-post-detail.png
   :alt: Post detail

d) Making Changes
-----------------

**Note:** If this is your first time using `Astro` or if you are unfamiliar with it, remember to restart the FE dev server after making API updates to ensure new API calls are made, as Astro caches your API requests.

- Visit http://localhost:8000/admin/astrowind_posts/awpost/1/change/ to update the first post.
- Update the `title` field under the `English` tab to: `Hello world`.
- Update the `title` field under the `Vietnamese` tab to: `Xin chao`.
- Save the post.
- Restart the FE dev server.
- Visit the blog page again (http://localhost:4321/en/blog). You will notice that nothing has changed. This is because the post has not been published yet, so the API call uses the published version, and the title remains unchanged.
- Visit http://localhost:8000/admin/astrowind_posts/awpost/1/change/ again. You will see `Item published (outdated).`.
- Click the `Publish` button to publish the post.
- Restart the FE dev server.
- Visit the blog page again. This time, you will see the updated title.

e) Create a New Post and Auto-Translate Using OpenAI ChatGPT
------------------------------------------------------------

- Open your BE project and add your OpenAI key to `OPENAI_API_KEY` in the `.env` file.
- Restart the BE server.
- Visit http://localhost:8000/admin/astrowind_posts/awpost/add/
- Fill out the post in `English`, for example:
   - Title: `My favorite post`
   - Author: `John Doe`
   - Content:

.. code-block:: text

    # How are you?

    This is the greeting, said in English.

- Updated date: Click on `today` and `now` to auto-populate.
- Click `Save and continue editing`.
- Click the `Translate missing` button to use AI to translate the post into other languages.
- Click `Publish` to publish the post.
- Restart the FE dev server.
- Visit http://localhost:4321/en/blog to see the new post at the top of the page.
- Click the post to view its details.
- Select other languages to see the post translated into different languages.


**And that's all about getting started with Django-headless-cms in conjunction with Astrowind. For more information,
explore the other sections of the documentation.**

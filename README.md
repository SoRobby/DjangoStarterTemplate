# DjangoStarterTemplate

A Django starter template for projects. **Note: This is a work in progress**.

## Setup

1. Clone the repository
2. Create a virtual python environment
3. Install the requirements from the "requirements.txt" file. Example using pip
    ```cdm
    pip install -r requirements.txt
    ```

3. Install the node modules from package.json. Navigate to \libs\npm\ which is where the package.json
    ```cdm
    npm install
    ```

4. Run `python manage.py migrate` to setup the local sqlite database. Run command from root folder of the project where
   the `manage.py` file is located.
5. Run `python manage.py runserver` to start the django server.
6. In a separate terminal, navigate to \libs\npm\ run `npm run build-watch` to start the webpack server that will
   compile Tailwind CSS in realtime.



## Utility Hooks

### Process form
1. Add the x-data of `x-data={ isProcessing: false }` to the form element.
2. Also on the form, @submit="isProcessing = validateForm('supportForm')"

```html
<form id="myForm" 
      action="#"
      method="POST"
      x-data="{ isProcessing: false}"
      @submit="isProcessing = validateForm('supportForm')">
   ...   
</form>
```

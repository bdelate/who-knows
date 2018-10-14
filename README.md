# Who Knows
Django based question and answer site similar to Stack Overflow or Quora

More information on the creation of 'Who Knows' is available here: [Who Knows - Info](https://www.grokmycode.com/portfolio/whoknows)

A live demo of 'Who Knows' is available here: [Who Knows - Live demo](https://whoknows.grokmycode.com)

Functionality:

* Asking and answering questions.
* Commenting on questions and answers.
* Up voting questions, answers and comments.
* Accepting answers as being correct.
* Tagging questions along with filtering questions by tag.
* Filtering for questions with no answers, accepted answers etc.
* Text based searching.
* User profiles including statistics based on votes received for questions, answers and comments.

### Dev setup
The docker image uses Python as its base and then manually installs node and npm for use with the Sass files.

```
docker-compose build
docker-compose run web python ./whoknows/manage.py migrate --settings=whoknows.settings.dev
docker-compose run web python ./whoknows/manage.py createsuperuser --settings=whoknows.settings.dev
docker-compose up
```

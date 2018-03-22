const feedbackContent = document.getElementById('feedback-content'),
    feedbackContainer = document.getElementById('feedback-container'),
    xhr = new XMLHttpRequest();

class Handler {

    constructor(container) {
        container.addEventListener('click', event => this.delegator(event));
    }

    delegator(event) {
        event.preventDefault();
        if (userAuthenticated === 'True') {
            let element = event.target;
            if (element.classList.contains('display-form')) {
                this.displayForm(element);
            } else if (element.classList.contains('submit-vote')) {
                this.submitForm(element);
                element.parentElement.setAttribute('hidden', 'hidden');
                this.updateVoteTotal(element);
            } else if (element.classList.contains('submit-post')) {
                this.submitForm(element);
                element.parentElement.setAttribute('hidden', 'hidden');
                this.displayNewPost(element);
            } else if (element.classList.contains('submit-accept')) {
                this.submitForm(element);
                this.toggleAcceptedAnswer(element);
            }
        } else {
            feedbackContent.innerHTML = '&times;  To do this you need to login or signup'
            feedbackContainer.style.display = 'block';
        }
    }

    displayForm(element) {
        let formElement = element.parentElement.querySelector('.form');
        formElement.removeAttribute('hidden');
        formElement.content.value = '';
        // Edge browser issue workaround: button sometimes isn't displayed
        formElement.querySelector('input[type="button"]').style.visibility = 'visible';
    }

    submitForm(element) {
        let formElement = element.parentElement,
            formData = new FormData(formElement),
            url = formElement['form-url'].value;
        xhr.open('POST', url, true);
        xhr.setRequestHeader("X-CSRFToken", formElement.csrfmiddlewaretoken.value);
        xhr.send(formData);
    }

    displayNewPost(element) {
        let formElement = element.parentElement,
            container = document.createElement('div'),
            content = document.createElement('p'),
            parent = formElement.parentElement.parentElement;
        container.classList.add('new-post')
        content.textContent = formElement.content.value;
        container.appendChild(content);
        parent.insertBefore(container, formElement.parentElement);
    }

    updateVoteTotal(element) {
        let formElement = element.parentElement,
            operation = formElement.operation.value,
            voteTotalElement = formElement.parentElement.querySelector('.vote-total');
        voteTotalElement.textContent = parseInt(voteTotalElement.textContent) + parseInt(operation);
    }

    toggleAcceptedAnswer(element) {
        let formElement = element.parentElement,
            container = document.getElementById('answer-section-' + formElement.answer_id.value);
        // the currently accepted answer was clicked, therefore unaccept it
        if (formElement.classList.contains('accept__form--accepted')) {
            document.getElementById('accept-flag-' + formElement.answer_id.value).style.display = 'none';
            container.classList.toggle('accepted');
            formElement.classList.remove('accept__form--accepted');
            formElement.classList.add('accept__form');
            element.value = 'Accept answer';
            element.classList.remove('btn__down');
            element.classList.add('btn__up');
        } else { // an unaccepted answer has been clicked
            let acceptedAnswer = document.querySelector('.accept__form--accepted');
            // unnacept the currently accepted answer (if one exists)
            if (acceptedAnswer !== null) {
                let acceptedAnswerContainer = document.getElementById('answer-section-' + acceptedAnswer.answer_id.value);
                document.getElementById('accept-flag-' + acceptedAnswer.answer_id.value).style.display = 'none';
                acceptedAnswerContainer.classList.remove('accepted');
                acceptedAnswer.classList.remove('accept__form--accepted');
                acceptedAnswer.classList.add('accept__form');
                acceptedAnswer.querySelector('input[name="submit"]').value = 'Accept answer';
                acceptedAnswer.querySelector('input[name="submit"]').classList.remove('btn__down');
                acceptedAnswer.querySelector('input[name="submit"]').classList.add('btn__up');
            }
            // accept the clicked answer
            document.getElementById('accept-flag-' + formElement.answer_id.value).style.display = 'block';
            container.classList.toggle('accepted');
            formElement.classList.remove('accept__form');
            formElement.classList.add('accept__form--accepted');
            element.value = 'Unaccept answer';
            element.classList.add('btn__down');
        }
    }
}

for (let container of document.querySelectorAll('.create-post, .stat, .submit-accept')) {
    new Handler(container);
}

// hide feedback section when feedback-content is clicked
feedbackContent.addEventListener('click', () => {feedbackContainer.style.display = 'none'});

// ajax response received
xhr.onload = function() {
    let responseObject = JSON.parse(xhr.responseText);
    feedbackContent.innerHTML = '&times;  ' + responseObject['response'];
    feedbackContainer.style.display = 'block';
}

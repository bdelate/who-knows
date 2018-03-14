var xhr = new XMLHttpRequest(),
    id_answer_form = document.getElementById('id_answer_form'),
    id_display_answer_form = document.getElementById('id_display_answer_form')
    id_answers = document.getElementById('id_answers'),
    feedbackContainer = document.getElementById('feedback-container'),
    id_feedback = document.getElementById('id_feedback');

function submit_vote_form(e) {
    e.preventDefault();
    if (user_authenticated == 'True') {
        var form = new FormData(e.target);
        xhr.open('POST', e.target.form_url.value, true);
        xhr.setRequestHeader("X-CSRFToken", e.target.csrfmiddlewaretoken.value);
        xhr.send(form);
        e.target.setAttribute('hidden', 'hidden');
        object_id = e.target.object_id.value;
        vote_type = e.target.vote_type.value;
        operation = e.target.operation.value;
        vote_total_element = document.getElementById(vote_type + "_vote_total_" + object_id)
        vote_total_element.innerText = parseInt(vote_total_element.innerText) + parseInt(operation);
    } else {
        id_feedback.innerHTML = '&times;  To do this you need to login or signup'
        feedbackContainer.style.display = 'block';
    }
}

function display_new_comment(section, content) {
    var comment = document.createElement('div');
    comment.classList.add('comment');
    section.appendChild(comment);
    var p_content = document.createElement('p');
    p_content.innerText = content;
    comment.appendChild(p_content);
    var p_meta = document.createElement('p');
    p_meta.innerText = 'Commented by: Me - Just now';
    comment.appendChild(p_meta);
    var hr = document.createElement('hr');
    section.appendChild(hr);
}

function display_new_answer(content) {
    id_answer_form.setAttribute('hidden', 'hidden');
    var answer = document.createElement('div');
    answer.classList.add('answer');

    var layout = document.createElement('div');
    layout.classList.add('layout');
    answer.appendChild(layout);

    var layout__upper = document.createElement('div');
    layout__upper.classList.add('layout__upper');
    layout.appendChild(layout__upper);

    var p_content = document.createElement('p');
    p_content.innerText = content;
    layout__upper.appendChild(p_content);
    var p_meta = document.createElement('p');
    p_meta.innerText = 'Answered by: Me - Just now';
    layout__upper.appendChild(p_meta);

    id_answers.appendChild(answer);
}

function submit_comment_form(e) {
    e.preventDefault();
    var form = new FormData(e.target);
    xhr.open('POST', comment_url, true);
    xhr.setRequestHeader("X-CSRFToken", e.target.csrfmiddlewaretoken.value);
    xhr.send(form);
    e.target.setAttribute('hidden', 'hidden');
    display_new_comment(e.target.parentElement, e.target.content.value)
}

function submit_answer_form(e) {
    e.preventDefault();
    var form = new FormData(id_answer_form);
    xhr.open('POST', e.target.create_answer_url.value, true);
    xhr.setRequestHeader("X-CSRFToken", e.target.csrfmiddlewaretoken.value);
    xhr.send(form);
}

// If accepted answer was clicked, unnacept it
// else if a different answer was clicked, unnacept the accepted answer (if there is one)
// and accept the clicked answer. Lastly, update the answer on the server via ajax
function toggle_accepted_answer(e) {
    e.preventDefault();
    var container = document.getElementById('answer-section-' + e.target.answer_id.value);
    if (e.target.classList.contains('accept__form--accepted')) {
        document.getElementById('accept-flag-' + e.target.answer_id.value).style.display = 'none';
        container.classList.toggle('accepted');
        e.target.classList.remove('accept__form--accepted');
        e.target.classList.add('accept__form');
        e.target.querySelector('input[name="submit"]').value = 'Accept answer';
        e.target.querySelector('input[name="submit"]').classList.remove('btn__down');
        e.target.querySelector('input[name="submit"]').classList.add('btn__up');
    } else {
        var accepted_answer = document.querySelector('.accept__form--accepted');
        if (accepted_answer !== null) {
            var accepted_answer_container = document.getElementById('answer-section-' + accepted_answer.answer_id.value);
            document.getElementById('accept-flag-' + accepted_answer.answer_id.value).style.display = 'none';
            accepted_answer_container.classList.remove('accepted');
            accepted_answer.classList.remove('accept__form--accepted');
            accepted_answer.classList.add('accept__form');
            accepted_answer.querySelector('input[name="submit"]').value = 'Accept answer';
            accepted_answer.querySelector('input[name="submit"]').classList.remove('btn__down');
            accepted_answer.querySelector('input[name="submit"]').classList.add('btn__up');
        }
        document.getElementById('accept-flag-' + e.target.answer_id.value).style.display = 'block';
        container.classList.toggle('accepted');
        e.target.classList.remove('accept__form');
        e.target.classList.add('accept__form--accepted');
        e.target.querySelector('input[name="submit"]').value = 'Unaccept answer';
        e.target.querySelector('input[name="submit"]').classList.add('btn__down');
    }

    var form = new FormData(e.target);
    xhr.open('POST', e.target.form_url.value, true);
    xhr.setRequestHeader("X-CSRFToken", e.target.csrfmiddlewaretoken.value);
    xhr.send(form);
}

// ajax response received
xhr.onload = function() {
    var responseObject = JSON.parse(xhr.responseText);
    id_feedback.innerHTML = '&times;  ' + responseObject['response'];
    feedbackContainer.style.display = 'block';
    if (xhr.status == 200) {
        if (responseObject['type'] == 'answer') {
            display_new_answer(document.getElementById("id_answer-content").value)
        }
    } else if (xhr.status == 400) {
        if (responseObject['response'] == 'login required') {
            id_feedback.innerHTML = '&times;  To do this you need to login or signup'
            feedbackContainer.style.display = 'block';
        }
    }
}

// event handlers /////////////////////////////////////////////////////////
id_answer_form.addEventListener('submit', function(e) { submit_answer_form(e); });

// add a submit listener to every vote form (which will include question, comment and answer vote forms)
vote_forms = document.getElementsByClassName('vote-form');
for (var i=0; i<vote_forms.length; i++) {
    vote_forms[i].addEventListener('submit', function(e) { submit_vote_form(e); });
}

// add a submit listener to every comment form (which will include question and answer comment forms)
comment_forms = document.getElementsByClassName('comment_form');
for (var i=0; i<comment_forms.length; i++) {
    comment_forms[i].addEventListener('submit', function(e) { submit_comment_form(e); });
}

// event listeners for every display_comment_form link (the question plus every answer has one of these)
display_comment_form_links = document.getElementsByClassName('display_comment_form');
for (var i=0; i<display_comment_form_links.length; i++) {
    display_comment_form_links[i].addEventListener('click', function(e) {
        if (user_authenticated == 'True') {
            e.preventDefault();
            comment_form = e.target.parentElement.querySelector('.comment_form');
            comment_form.removeAttribute('hidden');
            comment_form.content.value = '';
        } else {
            id_feedback.innerHTML = '&times;  To do this you need to login or signup'
            feedbackContainer.style.display = 'block';
        }
    });
}

// event listeners for every accept answer form
accept_forms = document.querySelectorAll('div.accept form');
for (var i=0; i<accept_forms.length; i++) {
    accept_forms[i].addEventListener('submit', function(e) { toggle_accepted_answer(e); });
}

id_display_answer_form.addEventListener('click', function(e) {
    if (user_authenticated == 'True') {
        e.preventDefault();
        document.getElementById("id_answer-content").value = '';
        id_answer_form.removeAttribute('hidden');
        id_answer_form.scrollIntoView();
    } else {
        id_feedback.innerHTML = '&times;  To do this you need to login or signup'
        feedbackContainer.style.display = 'block';
    }
});

// hide feedback section when id_feedback is clicked
id_feedback.addEventListener('click', function(e) {
    feedbackContainer.style.display = 'none';
});

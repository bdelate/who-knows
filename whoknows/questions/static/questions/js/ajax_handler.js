var xhr = new XMLHttpRequest(),
    id_login_redirect = document.getElementById('id_login_redirect'),
    id_answer_form = document.getElementById('id_answer_form'),
    id_display_answer_form = document.getElementById('id_display_answer_form')
    id_answers = document.getElementById('id_answers');

function submit_vote_form(e) {
    e.preventDefault();
    if (user_authenticated == 'True') {
        var form = new FormData(e.srcElement);
        xhr.open('POST', form.get('form_url'), true);
        xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
        xhr.send(form);
        e.srcElement.parentElement.setAttribute('hidden', 'hidden');
        object_id = form.get('object_id');
        vote_type = form.get('vote_type');
        operation = form.get('operation');
        vote_total_element = document.getElementById(vote_type + "_vote_total_" + object_id)
        vote_total_element.innerText = parseInt(vote_total_element.innerText) + parseInt(operation);
    } else {
        id_login_redirect.removeAttribute('hidden');
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
    id_answers.appendChild(answer);
    var p_content = document.createElement('p');
    p_content.innerText = content;
    answer.appendChild(p_content);
    var p_meta = document.createElement('p');
    p_meta.innerText = 'Answered by: Me - Just now';
    answer.appendChild(p_meta);
    var hr = document.createElement('hr');
    id_answers.appendChild(hr);
}

function submit_comment_form(e) {
    e.preventDefault();
    var form = new FormData(e.srcElement);
    xhr.open('POST', comment_url, true);
    xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
    xhr.send(form);
    e.srcElement.setAttribute('hidden', 'hidden');
    display_new_comment(e.srcElement.parentElement, form.get('content'))
}

function submit_answer_form(e) {
    e.preventDefault();
    var form = new FormData(id_answer_form);
    xhr.open('POST', form.get('create_answer_url'), true);
    xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
    xhr.send(form);
}

// ajax response received
xhr.onload = function() {
    var responseObject = JSON.parse(xhr.responseText);
    document.getElementById('id_feedback').innerHTML = responseObject['response'];
    if (xhr.status == 200) {
        if (responseObject['type'] == 'answer') {
            display_new_answer(document.getElementById("id_answer-content").value)
        }
    } else if (xhr.status == 400) {
        if (responseObject['response'] == 'login required') {
            id_login_redirect.removeAttribute('hidden');
        }
    }
}

// event handlers /////////////////////////////////////////////////////////
id_answer_form.addEventListener('submit', function(e) { submit_answer_form(e); });

// add a submit listener to every vote form (which will include question, comment and answer vote forms)
vote_forms = document.getElementsByClassName('vote_form');
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
            comment_form = e.srcElement.parentElement.querySelector('.comment_form');
            comment_form.removeAttribute('hidden');
            comment_form.content.value = '';
        } else {
            id_login_redirect.removeAttribute('hidden');
        }
    });
}

id_display_answer_form.addEventListener('click', function(e) {
    if (user_authenticated == 'True') {
        document.getElementById("id_answer-content").value = '';
        id_answer_form.removeAttribute('hidden');
    } else {
        id_login_redirect.removeAttribute('hidden');
    }
});

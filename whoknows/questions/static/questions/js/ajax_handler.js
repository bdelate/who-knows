var xhr = new XMLHttpRequest(),
    id_vote_form = document.getElementById('id_vote_form'),
    num_votes = parseInt(document.getElementById('id_num_question_votes').innerText),
    id_question_comment_form = document.getElementById('id_question_comment_form'),
    id_display_question_comment_form = document.getElementById('id_display_question_comment_form');

function submit_vote_form(e) {
    e.preventDefault();
    var form = new FormData(id_vote_form);
    xhr.open('POST', form.get('form_url'), true);
    xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
    xhr.send(form);
    document.getElementById('id_vote_section').innerHTML = '';
}

function display_new_comment(section, content) {
    id_question_comment_form.setAttribute('hidden', 'hidden');
    var p_content = document.createElement('p');
    p_content.innerText = content;
    document.getElementById(section).appendChild(p_content);
    var p_meta = document.createElement('p');
    p_meta.innerText = 'Commented by: Me - Just now';
    document.getElementById(section).appendChild(p_meta);
    var hr = document.createElement('hr');
    document.getElementById(section).appendChild(hr);
}

function submit_comment_form(e) {
    e.preventDefault();
    var form = new FormData(id_question_comment_form);
    xhr.open('POST', comment_url, true);
    xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
    xhr.send(form);
}

function update_vote_total(responseObject) {
    if (responseObject['response'] == 'Thanks for your vote') {
        document.getElementById('id_num_question_votes').innerText = num_votes + 1;
    } else if (responseObject['response'] == 'Your vote has been removed') {
        document.getElementById('id_num_question_votes').innerText = num_votes - 1;
    }
}

// ajax response received
xhr.onload = function() {
    var responseObject = JSON.parse(xhr.responseText);
    document.getElementById('id_feedback').innerHTML = responseObject['response'];
    if (xhr.status == 200) {
        if (responseObject['type'] == 'comment') {
            display_new_comment('id_question_comment_section', document.getElementById("id_content").value);
        } else if (responseObject['type'] == 'vote') {
            update_vote_total(responseObject);
        }
    }
}

// event handlers /////////////////////////////////////////////////////////

id_question_comment_form.addEventListener('submit', function(e) { submit_comment_form(e); });

if (id_vote_form !== null) {
    id_vote_form.addEventListener('submit', function(e) { submit_vote_form(e); });
}

id_display_question_comment_form.addEventListener('click', function(e) {
    document.getElementById("id_content").value = '';
    id_question_comment_form.removeAttribute('hidden');
});

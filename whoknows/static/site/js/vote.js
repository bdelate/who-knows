var xhr = new XMLHttpRequest(),
    id_vote_form = document.getElementById('id_vote_form'),
    num_votes = parseInt(document.getElementById('id_num_question_votes').innerText);

if (id_vote_form !== null) {
    id_vote_form.addEventListener('submit', function(e) {
        e.preventDefault();
        var form = new FormData(id_vote_form);
        xhr.open('POST', form.get('form_url'), true);
        xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
        xhr.send(form);
    });
}

// ajax response received
xhr.onload = function() {
    var responseObject = JSON.parse(xhr.responseText);
    document.getElementById('id_feedback').innerHTML = responseObject['response'];
    if (xhr.status == 200) {
        document.getElementById('id_vote_section').innerHTML = '';
        if (responseObject['response'] == 'Thanks for your vote') {
            document.getElementById('id_num_question_votes').innerText = num_votes + 1;
        } else if (responseObject['response'] == 'Your vote has been removed') {
            document.getElementById('id_num_question_votes').innerText = num_votes - 1;
        }
    }
}

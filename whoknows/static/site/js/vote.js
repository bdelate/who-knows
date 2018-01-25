var xhr = new XMLHttpRequest(),
    id_vote_form = document.getElementById('id_vote_form');

if (id_vote_form !== null) {
    id_vote_form.addEventListener('submit', function(e) {
        e.preventDefault();
        var form = new FormData(id_vote_form);
        xhr.open('POST', up_vote_url, true);
        xhr.setRequestHeader("X-CSRFToken", form.get('csrfmiddlewaretoken'));
        xhr.send(form);
    });
}

xhr.onload = function() {
    var responseObject = JSON.parse(xhr.responseText);
    document.getElementById('id_feedback').innerHTML = responseObject['response'];
    if (responseObject['response'] == 'Thanks for your vote') {
        var num_votes = parseInt(document.getElementById('id_num_question_votes').innerText);
        document.getElementById('id_num_question_votes').innerText = num_votes + 1;
        document.getElementById('id_vote_form_section').innerHTML = '';
    }
}

$("input.correct").on('click', function (ev) {
    console.log("correct");
    const request = new Request(
    'http://127.0.0.1:8000/correct/',
    {
        method: 'POST',
        headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question_id: $(this).data("qid"), answer_id : $(this).data("aid")}),
    }
    );

    fetch(request).then(
        console.log("ok")
    );
});
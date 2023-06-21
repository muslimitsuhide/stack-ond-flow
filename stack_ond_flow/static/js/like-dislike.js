async function elementUpdate(selector) {
    try {
      var html = await (await fetch(location.href)).text();
      var newdoc = new DOMParser().parseFromString(html, 'text/html');
      document.querySelector(selector).outerHTML = newdoc.querySelector(selector).outerHTML;
      console.log('Элемент '+selector+' был успешно обновлен');
      return true;
    } catch(err) {
      console.log('При обновлении элемента '+selector+' произошла ошибка:');
      console.dir(err);
      return false;
    }
  }
  
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  
  const csrftoken = getCookie('csrftoken');
  
  $("button.btn-up").on('click', function (ev) {
      console.log($(this).data("id"))
      let rating = $("#rating-" + $(this).data("id")).text();
      console.log(rating);
      const request = new Request(
      'http://127.0.0.1:8000/vote/',
      {
          method: 'POST',
          headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question_id: $(this).data("id"), vote : "+"}),
      }
      );
  
      fetch(request).then(
          response_row => response_row.json().then(
              response_json => {
              console.log("click");
              if (response_json.status === "error") {
                  console.log(`error: ${response_json.message}`);
              } else {
                  console.log(request);
                  $("#rating-" + $(this).data("id")).text(response_json.new_rating);
                  if(response_json.new_rating > rating) {
                       $("#btn-up-" + $(this).data("id")).css({"border": "solid"})
                       $("#btn-down-" + $(this).data("id")).css({"border": "none"})
                  } else {
                      $("#btn-up-" + $(this).data("id")).css({"border": "none"})
                  }
                  //btn_like.next().html(response_json.new_rating);
                  console.log(response_json.new_rating)
              }
          })
      );
  });
  
  $("button.btn-down").on('click', function (ev) {
      console.log($(this).data("id"))
      let rating = $("#rating-" + $(this).data("id")).text();
      const request = new Request(
      'http://127.0.0.1:8000/vote/',
      {
          method: 'POST',
          headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question_id: $(this).data("id"), vote : "-"}),
      }
      );
  
      fetch(request).then(
          response_row => response_row.json().then(
              response_json => {
              console.log("click");
              if (response_json.status === "error") {
                  console.log(`error: ${response_json.message}`);
              } else {
                  console.log(request);
                   $("#rating-" + $(this).data("id")).text(response_json.new_rating);
                  if(response_json.new_rating < rating) {
                      $("#btn-down-" + $(this).data("id")).css({"border": "solid"})
                      $("#btn-up-" + $(this).data("id")).css({"border": "none"})
                  } else {
                      $("#btn-down-" + $(this).data("id")).css({"border": "none"})
                  }
                  console.log(response_json.new_rating)
              }
          })
      );
  });
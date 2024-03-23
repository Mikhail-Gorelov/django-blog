let url = window.location.href;
let code = url.split("page=");
if (code[1] === "1") {
  buttons_1(code);
}
if (code[1] === "2") {
  buttons_2(code);
}
if (code[1] === "3") {
  buttons_3(code);
}

function a_j_a_x(old_code, new_code) {
  $.ajax({
    url: new_code,
    type: "GET",
    success: success_process(new_code),
    error: error_process(old_code),
  })

}
function success_process(code) {
  window.location.href = code;
}
function error_process(code) {
  window.location.href = code;
}

function buttons_3(code) {
   let a = document.getElementById('previousHref');
   code[1] = "page=2";
   a.href = code[0] + code[1];
   $('#previousHref').click(function(){ a_j_a_x(code, a.href);  });
  let b = document.getElementById('nextHref');
  code[1] = "page=3";
  b.href = code[0] + code[1];
  $('#nextHref').click(function(){ a_j_a_x(code, b.href);  });
}

function buttons_2(code) {
   let a = document.getElementById('previousHref');
   code[1] = "page=1";
   a.href = code[0] + code[1];
   $('#previousHref').click(function(){ a_j_a_x(code, a.href);  });
  let b = document.getElementById('nextHref');
  code[1] = "page=3";
  b.href = code[0] + code[1];
  $('#nextHref').click(function(){ a_j_a_x(code, b.href);  });
}
function buttons_1(code) {
   let a = document.getElementById('previousHref');
   code[1] = "page=1";
   a.href = code[0] + code[1];
   $('#previousHref').click(function(){ a_j_a_x(code, a.href);  });
  let b = document.getElementById('nextHref');
  code[1] = "page=2";
  b.href = code[0] + code[1];
  $('#nextHref').click(function(){ a_j_a_x(code, b.href);  });
}


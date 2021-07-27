let url = window.location.href;
console.log(url)
let code = url.split("page=");
if (code[1] === "1") {
  //a_j_a_x(code, buttons_1); // buttons_1(code)
  buttons_1(code);
}
if (code[1] === "2") {
  //a_j_a_x(code, buttons_2); // buttons_2(code)
  buttons_2(code);
}
if (code[1] === "3") {
  //a_j_a_x(code, buttons_3); // buttons_3(code)
  buttons_3(code);
}
// $('#previousHref').click(function(){ Prevfunc();  });
// function Prevfunc() {
//   alert("Previous")
// }
// $('#nextHref').click(function(){ Nextfunc();  });
// function Nextfunc() {
//   alert("Next")
// }

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





// old style, works good, but incorrectly
// function buttons_3(code) {
//    let a = document.getElementById('previousHref');
//    code[1] = "page=2";
//    a.href = code[0] + code[1];
//   let b = document.getElementById('nextHref');
//   code[1] = "page=3";
//   b.href = code[0] + code[1];
// }
//
// function buttons_2(code) {
//    let a = document.getElementById('previousHref');
//    code[1] = "page=1";
//    a.href = code[0] + code[1];
//   let b = document.getElementById('nextHref');
//   code[1] = "page=3";
//   b.href = code[0] + code[1];
// }
// function buttons_1(code) {
//    let a = document.getElementById('previousHref');
//    code[1] = "page=1";
//    a.href = code[0] + code[1];
//   let b = document.getElementById('nextHref');
//   code[1] = "page=2";
//   b.href = code[0] + code[1];
// }

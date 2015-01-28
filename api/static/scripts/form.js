function touchButton(param) {

          $.ajax({
            url: '/approved?choice=' + param,
            success: function (ret) {
              //alert('JSON posted: ' + JSON.stringify(ret));
            }
          });

}

function setGender(param) {
    $.ajax({
            url: '/set_gender?gender=' + param,
            success: function (ret) {
              //alert('JSON posted: ' + JSON.stringify(ret));
            }
          });
}

function setAge(param) {
    $.ajax({
            url: '/set_age?age=' + param,
            success: function (ret) {
              //alert('JSON posted: ' + JSON.stringify(ret));
            }
          });
}
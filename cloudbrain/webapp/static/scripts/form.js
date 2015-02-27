function touchButton(param) {

          $.ajax({
            url: '/approved?choice=' + param,
            success: function (ret) {
              //alert('JSON posted: ' + JSON.stringify(ret));
            }
          });

}

function setTag(param) {
    $.ajax({
            url: '/set_tag?number=' + param,
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

$(document).on('ready', function () {
  var _data = {
    consent : 'no',
    headset : 0,
    age: 0,
    gender: 'NA'
  };

  $('#tag').change(function () {
    _data.headset = $(this).val();
  });

  $('.btn-toggle button').click(function(e) {
    e.preventDefault();
    _data.consent = $(this).data('value');
    $(this).removeClass('noselected');
    $(this).siblings().addClass('noselected');
    $(this)[0].blur();
  });

  $('#age').change(function () {
    _data.age = $(this).val();
  });

  $('#gender').change(function () {
    _data.gender = $(this).val();
  });

  $('#submit').on('click', function (e) {
    e.preventDefault();
    $('.alert-danger').hide();
    $(this)[0].blur();
    if (_data.headset<1) {
      console.log('not posting because no headset');
      $('.alert.headset').show();
      return;
    }
    console.log('posting things');
    $.post('/form-content', _data)
    .done(function () {
      window.location = '/thank-you';
    })
    .fail(function () {
      console.log('failed');
    });
  });

});


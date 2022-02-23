$("#nav__menu").mousedown(function (e) {
    e.preventDefault();
  });
  let focused = false;
  $("#toggler").click(function () {
    if (focused) {
      $("#toggler").blur();
      focused = false;
    } else {
      focused = true;
    }
  });
  $("#toggler").focusout(function () {
    focused = false;
  });
  
  
  // For channel name edit

  $('#name-edit-icon').click(function(){
    $('#channel-name-edit-text').show();
    $('#name-save-icon').show();
    $('#channel-name').hide();
    $('#name-edit-icon').hide();
  })


  // For channel profile pic edit

  $('#profile-edit-icon').click(function(){
    $('#profile-edit-icon').hide();
    $('#profile-pic-form').show();
    $('#channel-name-edit-text').hide();
    $('#name-save-icon').hide();
    $('#channel-name').show();
    $('#name-edit-icon').show();
  })
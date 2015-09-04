var matter = new Matter('tessellate', {localServer:true});
console.log('matter:', matter);
//Set logged in status when dom is loaded
document.addEventListener("DOMContentLoaded", function(event) { 
  setStatus();
});
//Set status styles
function setStatus() {
  var statusEl = document.getElementById("status");
  var logoutButton = document.getElementById("logout-btn");

  if(matter.isLoggedIn){
    statusEl.innerHTML = "True";
    statusEl.style.color = 'green';
    // statusEl.className = statusEl.className ? ' status-loggedIn' : 'status-loggedIn';
    logoutButton.style.display='inline';
  } else {
    statusEl.innerHTML = "False";
    statusEl.style.color = 'red';
    logoutButton.style.display='none';
  }
}

function login(){
  var username = document.getElementById('login-username').value;
  var password = document.getElementById('login-password').value;
  matter.login({username:username, password:password}).then(function(loginInfo){
    console.log('successful login:', loginInfo);
    setStatus();
  }, function(err){
    console.error('login() : Error logging in:', err);
  });   
}
function logout(){
  matter.logout().then(function(){
    console.log('successful logout');
    setStatus();
  }, function(err){
    console.error('logout() : Error logging out:', err);
  });   
}
function signup(){
  var name = document.getElementById('signup-name').value;
  var username = document.getElementById('signup-username').value;
  var email = document.getElementById('signup-email').value;
  var password = document.getElementById('signup-password').value;

  matter.signup().then(function(){
    console.log('successful logout');
    setStatus();
  }, function(err){
    console.error('logout() : Error logging out:', err);
  });   
}

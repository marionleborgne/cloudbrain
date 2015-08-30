# Matter

[![Travis build status](https://travis-ci.org/KyperTech/matter.svg?branch=master)](https://travis-ci.org/kypertech/matter)
[![Code Climate](https://codeclimate.com/github/KyperTech/matter/badges/gpa.svg)](https://codeclimate.com/github/kypertech/matter)
[![Test Coverage](https://codeclimate.com/github/KyperTech/matter/badges/coverage.svg)](https://codeclimate.com/github/KyperTech/matter)
[![Dependency Status](https://david-dm.org/kypertech/matter.svg)](https://david-dm.org/kypertech/matter)
[![devDependency Status](https://david-dm.org/kypertech/matter/dev-status.svg)](https://david-dm.org/kypertech/matter#info=devDependencies)

Common Web Application functionality such as user authentication and local/session/token storage. Matter is a javascript library that communicates with [Tessellate](https://github.com/KyperTech/tessellate).

## Getting Started

Using matter requires having created an application on [Tessellate](http://tessellate.elasticbeanstalk.com).

### Browser
1. Include the Matter library using one of the following:
  #### CDN
  Add script tag to index.html:
    
    ```html
    <script src="http://cdn.kyper.io/js/matter/0.0.2/matter.bundle.js"></script>
    ```

  #### Bower
  Run `bower install --save kyper-matter`


1. Start using Matter by providing the name of the app you created on [Tessellate](http://tessellate.elasticbeanstalk.com).

  ```javascript
  //New matter object with the application name 'exampleApp'
  var matter = new Matter('exampleApp');
  //Login to account with username "test" and password "test"
  matter.login({username:"test", password:"test"}).then(function(user){
      console.log('User logged into exampleApp:', user);
  });
  ```

### ES6 or NodeJS
1. Run `npm install --save kyper-matter`
2. Start using matter:
```javascript
//New matter object with the application name 'exampleApp'
var matter = new Matter('exampleApp');
//Login to account with username "test" and password "test"
matter.login({username:"test", password:"test"}).then(function(user){
    console.log('User logged into exampleApp:', user);
});
```

## API Documentation

### Logout()
Log current user out
Example: 
```
Matter.logout().then(function(){ console.log('User logged out')});}
```

### Login()
Log user in provided username/email and password.

Example: 
```
Matter.login({username: 'test', password: 'test'})
.then(function(){ console.log('User logged in')});
```

###Signup()
Create a new user and login

Example: 
```
Matter.signup({username: 'test', name:'Test User', password: 'test'})
.then(function(){ console.log('User logged in')});
```

###getCurrentUser()
Get currently logged in user.

Example: 
```
Matter.getCurrentUser().then(function(){ console.log('User logged in')});
```

###getAuthToken()
Get Auth token for currently logged in user

Example: `var token = Matter.getAuthToken();`

## TODO
* Improve Documentation
* Change Password Method
* Run tests git pre-push
* More local storage capabilities
* Upload to cdn gulp task
* Version release gulp task


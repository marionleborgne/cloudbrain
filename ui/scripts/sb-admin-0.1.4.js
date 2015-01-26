/**
 * Spacebrew Admin Mixin for Javascript
 * --------------------------------
 *
 * This is an admin client mixim for the Spacebrew library. By passing the Spacebrew.Admin
 * object into the Spacebrew.Client library's extend() method your client application will also
 * connect to Spacebrew as an admin.
 *
 * Spacebrew is an open, dynamically re-routable software toolkit for choreographing interactive 
 * spaces. Or, in other words, a simple way to connect interactive things to one another. Learn 
 * more about Spacebrew here: http://docs.spacebrew.cc/
 *
 * Please note that this library only works will the Spacebrew.js library sb-1.0.4.min.js and 
 * above.
 *
 * Latest Updates:
 * - enable client apps to be extended to include admin privileges.
 * - added methods to handle admin messages and to update routes.
 * 
 * @author 		Julio Terra and Brett Renfer
 * @filename	sb-admin-0.1.4.js
 * @version 	0.1.4
 * @date 		April 8, 2013
 * 
 */

Spacebrew.Admin = {
	admin: {
		config: { 
			admin: true 
			, no_msgs: true
		} 
		, active: true
		, remoteAddress: undefined
		, clients: []
		, routes: []
	}
}

/*********************************
 ** ADMIN CONFIGURATION METHODS
 *********************************/

/**
 * Sends the admin config message to the Spacebrew server. This message resgisters
 * 		a client app as an admin app. This method is automatically called by the 
 * 		Spacebrew library if the library is extended with the admin mix-in before the
 * 		client is configured.
 * 		
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin.connectAdmin = function () {
	this.socket.send(JSON.stringify(this.admin.config));	
}

/**
 * Enables turning on or off configuration option for admin app to receive all
 * 		messages sent between clients. This option must be set before the 
 * 		Spacebrew server connection is made
 * 		
 * @param  {Boolean} get_msgs   Flag that sets admin message request on or off
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.getMsgs = function ( get_msgs ) {
	if (get_msgs == false) {
		config.no_msgs = false;
	} 
	else {
		config.no_msgs = true;		
	}
}

/*********************************
 ** EVENT CALLBACK METHODS STUBS
 *********************************/

/**
 * Override in your app to receive new client information, e.g. sb.onNewClient = yourFunction
 * Admin-related method.
 * 
 * @param {Object} client  			Object with client config details described below:
 *        - {String} name  				Name of client
 *        - {String} address 			IP address of client
 *        - {String} description 		Description of client
 *        - {Array} publish 			Array with all publish data feeds for client
 *        - {Array} subscribe  			Array with subscribe data feeds for client
 *        
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.onNewClient = function( client ){}

/**
 * Override in your app to receive updated information about existing client, e.g. sb.onNewClient = yourFunction
 * Admin-related method.
 * 
 * @param {Object} client  			Object with client config details described below
 *        - {String} name  				Name of client
 *        - {String} address 			IP address of client
 *        - {String} description 		Description of client
 *        - {Array} publish 			Array with all publish data feeds for client
 *        - {Array} subscribe  			Array with subscribe data feeds for client
 *        
 * @memberOf Spacebrew.Admin
 * @public
 */
// Spacebrew.Admin.onUpdateClient = function( name, address, description, pubs, subs ){}
Spacebrew.Admin.onUpdateClient = function( client ){}

/**
 * Override in your app to receive information about new routes, e.g. sb.onNewRoute = yourStringFunction
 * Admin-related method.
 * 
 * @param  {String} action 			Type of action route message, either add or remove
 * @param  {Object} pub 			Object with name of client name and address, publish name and type
 * @param  {Object} sub 			Object with name of client name and address, subscribe name and type
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.onUpdateRoute = function( action, pub, sub ){}

/**
 * Override in your app to receive client removal messages, e.g. sb.onCustomMessage = yourStringFunction
 * Admin-related method.
 * 
 * @param  {String} name  		Name of client being removed
 * @param  {String} address  	Address of client being removed
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.onRemoveClient = function( name, address ){}


/**********************************
 ** PRIVATE EVENT HANDLER METHODS
 **********************************/

/**
 * Handles admin messages received from the Spacbrew server. Routes the messages based on the
 * 		message type
 * @param  {Object} data Message object that contains an admin, config, remove, or route message
 * 
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._handleAdminMessages = function( data ){
	if (this.debug) console.log("[_handleAdminMessages] new message received ");

	if (data["admin"]) {
		// nothing to be done
	}

	else if (data["remove"]) {
		if (this.debug) console.log("[_handleAdminMessages] remove client message ", data["remove"]);
		for (var i = 0; i < data.remove.length; i ++) {
			this._onRemoveClient( data.remove[i] );
		}			
	}

	else if (data["route"]) {
		if (this.debug) console.log("[_handleAdminMessages] route update message ", data["route"]);
		var new_route = {
			route: {
				type: data.route.type,
				publisher: data.route.publisher,
				subscriber: data.route.subscriber				
			}
		}
		if ( data.route.type !== "remove" ){
			var bFound = false;
			for (var i = 0; i < this.admin.routes.length; i++) {
				// if route does not exists then create it, otherwise abort
				if (this._compareRoutes(new_route.route, this.admin.routes[i].route)){
					bFound = true;
					break;
				}
			}
			if ( !bFound ){
				this.admin.routes.push(new_route);
			}
		} else {
			for (var i = this.admin.routes.length - 1; i >= 0; i--) {
				// if route exists then remove it, otherwise abort
				if (this._compareRoutes(data.route, this.admin.routes[i].route)){
					this.admin.routes.splice(i,i);
					bFound = true;
					break;
				}
			}
		}
		this.onUpdateRoute( data.route.type, data.route.publisher, data.route.subscriber );
	} 

	else if (data instanceof Array || data["config"]) {
		if (this.debug) console.log("[_handleAdminMessages] handle client config message(s) ", data);

		if (data["config"]) data = [data];	
		for (var i = 0; i < data.length; i ++) {
			if (data[i]["config"]) {
				this._onNewClient(data[i].config);
			} 
		}
	}	
}

/**
 * Called when a new client message is received. It adds the client to this.admin.clients
 * 		array and then forwards the message to front-end callback methods.
 * 
 * @param {Object} client  			Object with client config details described below:
 *        - {String} name  				Name of client
 *        - {String} address 			IP address of client
 *        - {String} description 		Description of client
 *        - {Array} publish 			Array with all publish data feeds for client
 *        - {Array} subscribe  			Array with subscribe data feeds for client
 *                          
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._onNewClient = function( client ){
	var existing_client = false;

	this._setLocalIPAddress( client );

	for( var j = 0; j < this.admin.clients.length; j++ ){

		if ( this.admin.clients[j].name === client.name
			 && this.admin.clients[j].remoteAddress === client.remoteAddress ) {
			if (this.debug) console.log("existing client logged on " + client.name + " address " + client.remoteAddress);				

			existing_client = true;

			this.admin.clients[j].publish = client.publish;
			this.admin.clients[j].subscribe = client.subscribe;
			this.admin.clients[j].description = client.description;
			this.onUpdateClient( client );
		}
	}

	//if we did not find a matching client, then add this one
	if ( !existing_client ) {
		if (this.debug) console.log("new client logged on " + client.name + " address " + client.remoteAddress);				

		this.admin.clients.push( client );
		this.onNewClient( client );
	}
}

Spacebrew.Admin._onRemoveClient = function( client ){
	var existing_client = false;
	var clientIndex 	= -1;

	for( var j = 0; j < this.admin.clients.length; j++ ){

		if ( this.admin.clients[j].name === client.name
			 && this.admin.clients[j].remoteAddress === client.remoteAddress ) {
			if (this.debug) console.log("existing client logged on " + client.name + " address " + client.remoteAddress);				

			existing_client = true;
			clientIndex = j;
		}
	}

	//if we found a matching client, remove it
	if ( existing_client ) {
		if (this.debug) console.log("removed client " + client.name + " address " + client.remoteAddress);				

		this.admin.clients.splice( clientIndex, 1 );
	}

	// broadcast event regardless
	this.onRemoveClient( client.name, client.remoteAddress );
}

/**
 * Checks new client config messages to capture the IP address of the local application.
 * 		It first check if the current apps IP address has already been identified, if not
 * 		then it confirms that app name, and all publishers and subscribers match.
 * 		
 * @param {Object} client  			Object with client config details described below:
 *        - {String} name  				Name of client
 *        - {String} address 			IP address of client
 *        - {String} description 		Description of client
 *        - {Array} publish 			Array with all publish data feeds for client
 *        - {Array} subscribe  			Array with subscribe data feeds for client
 *                          
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._setLocalIPAddress = function ( client ) {
	var match_confirmed = true
		, cur_pub_sub = ["subscribe", "publish"]
		, client_config = []
		, local_config = []
		;

	// check if client already exists
	if (client.name === this._name && !this.admin.remoteAddress) {
		if ((client.publish.messages.length == this.client_config.publish.messages.length) &&
			(client.subscribe.messages.length == this.client_config.subscribe.messages.length)) {

			for (var j = 0; j < cur_pub_sub.length; j ++ ) {
				client_config = client[cur_pub_sub[j]].messages;
				local_config = this.client_config[cur_pub_sub[j]].messages;

				for (var i = 0; i < client_config.length; i ++ ) {
					if (!(client_config[i].name === local_config[i].name) ||
						!(client_config[i].type === local_config[i].type)) {
						match_confirmed = false;
						break;
					}	
				}									
			}	
			if (match_confirmed){
				this.admin.remoteAddress = client.remoteAddress;	
				if (this.debug) console.log("[_setLocalIPAddress] local IP address set to ", this.admin.remoteAddress);				
			}
		}
	}
}

/**********************************
 ** ROUTE HANDLER METHODS
 **********************************/

/**
 * Method that is used to add a route to the Spacebrew server
 * @param {String or Object} pub_client 	Publish client app name OR
 *                   						object with all publish information.
 * @param {String or Object} pub_address 	Publish app remote IP address OR
 *                   						object with all subscribe information.
 * @param {String} pub_name    				Publish name 
 * @param {String} sub_client  				Subscribe client app name
 * @param {String} sub_address 				Subscribe app remote IP address 
 * @param {String} sub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.addRoute = function ( pub_client, pub_address, pub_name, sub_client, sub_address, sub_name ){
	this._updateRoute("add", pub_client, pub_address, pub_name, sub_client, sub_address, sub_name);
}

/**
 * Method that is used to add a sub route to the Spacebrew server
 * @param {String} pub_name    				Publish name 
 * @param {String} sub_client  				Subscribe client app name
 * @param {String} sub_address 				Subscribe app remote IP address 
 * @param {String} sub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.addSubRoute = function ( pub_name, sub_client, sub_address, sub_name ){
	if (!this.admin.remoteAddress) return;
	this._updateRoute("add", this._name, this.admin.remoteAddress, pub_name, sub_client, sub_address, sub_name);
}

/**
 * Method that is used to add a pub route to the Spacebrew server
 * @param {String} sub_name    				Publish name 
 * @param {String} pub_client  				Subscribe client app name
 * @param {String} pub_address 				Subscribe app remote IP address 
 * @param {String} pub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.addPubRoute = function ( sub_name, pub_client, pub_address, pub_name){
	if (!this.admin.remoteAddress) return;
	this._updateRoute("add", pub_client, pub_address, pub_name, this._name, this.admin.remoteAddress, sub_name);
}

/**
 * Method that is used to remove a route from the Spacebrew server
 * @param {String or Object} pub_client 	Publish client app name OR
 *                   						object with all publish information.
 * @param {String or Object} pub_address 	Publish app remote IP address OR
 *                   						object with all subscribe information.
 * @param {String} pub_name    				Publish name 
 * @param {String} sub_client  				Subscribe client app name
 * @param {String} sub_address 				Subscribe app remote IP address 
 * @param {String} sub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.removeRoute = function ( pub_client, pub_address, pub_name, sub_client, sub_address, sub_name ){
	this._updateRoute("remove", pub_client, pub_address, pub_name, sub_client, sub_address, sub_name);
}

/**
 * Method that is used to remove a sub route from the Spacebrew server
 * @param {String} pub_name    				Publish name 
 * @param {String} sub_client  				Subscribe client app name
 * @param {String} sub_address 				Subscribe app remote IP address 
 * @param {String} sub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.removeSubRoute = function ( pub_name, sub_client, sub_address, sub_name ){
	if (!this.admin.remoteAddress) return;
	this._updateRoute("remove", this._name, this.admin.remoteAddress, pub_name, sub_client, sub_address, sub_name);
}

/**
 * Method that is used to remove a pub route from the Spacebrew server
 * @param {String} sub_name    				Publish name 
 * @param {String} pub_client  				Subscribe client app name
 * @param {String} pub_address 				Subscribe app remote IP address 
 * @param {String} pub_name    				Subscribe name
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.removePubRoute = function ( sub_name, pub_client, pub_address, pub_name){
	if (!this.admin.remoteAddress) return;
	this._updateRoute("remove", pub_client, pub_address, pub_name, this._name, this.admin.remoteAddress, sub_name);
}

/**
 * Method that handles both add and remove route requests. Responsible for parsing requests
 * and communicating with Spacebrew server
 * 
 * @param {String} type 					Type of route request, either "add" or "remove"
 * @param {String or Object} pub_client 	Publish client app name OR
 * @param {String or Object} pub_client 	Publish client app name OR
 *                   						object with all publish information.
 * @param {String or Object} pub_address 	Publish app remote IP address OR
 *                   						object with all subscribe information.
 * @param {String} pub_name    				Publish name 
 * @param {String} sub_client  				Subscribe client app name
 * @param {String} sub_address 				Subscribe app remote IP address 
 * @param {String} sub_name    				Subscribe name
 *
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._updateRoute = function ( type, pub_client, pub_address, pub_name, sub_client, sub_address, sub_name ){
	var new_route
		, route_type
		, subscribe
		, publish
		;

	// if request type is not supported then abort
	if (type !== "add" && type !== "remove") return;

	// check if pub and sub information was in first two arguments. If so then 
	if ((pub_client.clientName && pub_client.remoteAddress && pub_client.name && pub_client.type != undefined) &&
		(pub_address.clientName && pub_address.remoteAddress && pub_address.name && pub_address.type != undefined)) {
		new_route = {
			route: {
				type: type,
				publisher: pub_client,
				subscriber: pub_address				
			}
		}

		if (type === "add") {
			var bFound = false;
			for (var i = 0; i < this.admin.routes.length; i++) {
				// if route does not exists then create it, otherwise abort
				if (this._compareRoutes(new_route.route, this.admin.routes[i].route)){
					bFound = true;
					break;
				}
			}
			if ( bFound ){
				return;
			} else {
				this.admin.routes.push(new_route);
			}
		}

		else if (type === "remove") {
			var bFound = false;
			for (var i = this.admin.routes.length - 1; i >= 0; i--) {
				// if route exists then remove it, otherwise abort
				if (this._compareRoutes(new_route.route, this.admin.routes[i].route)){
					this.admin.routes.splice(i,i);
					bFound = true;
					break;
				}
			}
			if ( !bFound ){
				console.log("[_updateRoute] trying to remove route that does not exist");
				//return;
			}
		}

		// send new route information to spacebrew server
		if (this.debug) console.log("[_updateRoute] sending route to admin ", JSON.stringify(new_route));
		this.socket.send(JSON.stringify(new_route));
		return;
	}

	pub_type = this.getPublishType(pub_client, pub_address, pub_name);
	sub_type = this.getSubscribeType(sub_client, sub_address, sub_name);
	if (pub_type != sub_type || pub_type == false || pub_type == undefined) {
		if (this.debug) console.log("[_updateRoute] not routed :: types don't match - pub:" + pub_type + " sub:  " + sub_type);
		return;
	}

	publish = {
		clientName: pub_client,
		remoteAddress: pub_address,
		name: pub_name,
		type: pub_type
	}
	if (this.debug) console.log("[_updateRoute] created pub object ", publish);

	subscribe = {
		clientName: sub_client,
		remoteAddress: sub_address,
		name: sub_name,
		type: sub_type
	}
	if (this.debug) console.log("[_updateRoute] created sub object ", subscribe);

	// call itself with publish and subscribe objects properly formatted
	this._updateRoute(type, publish, subscribe);
}

/**
 * Compares two different routes.
 * 	
 * @param  {Object} route_a   Route description that contains client name and remote address, 
 *                            route name and type
 * @param  {Object} route_b   Route description that contains client name and remote address, 
 *                            route name and type
 * @return {Boolean} 		  Returns true of match is valid, false otherwise
 *
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._compareRoutes = function (route_a, route_b){
	// publisher
	var bPublisherMatch = false;

	if ((route_a.publisher.clientName === route_b.publisher.clientName) &&
		(route_a.publisher.name === route_b.publisher.name) &&
		(route_a.publisher.type === route_b.publisher.type) &&
		(route_a.publisher.remoteAddress === route_b.publisher.remoteAddress)) {
		bPublisherMatch = true;
	}

	// subscriber
	var bSubscriberMatch = false;
	if ((route_a.subscriber.clientName === route_b.subscriber.clientName) &&
		(route_a.subscriber.name === route_b.subscriber.name) &&
		(route_a.subscriber.type === route_b.subscriber.type) &&
		(route_a.subscriber.remoteAddress === route_b.subscriber.remoteAddress)) {
		bSubscriberMatch = true;
	}
	return bSubscriberMatch && bPublisherMatch;
}

/**********************************
 ** INSPECT CLIENT METHODS
 **********************************/

/**
 * Returns the type of a publisher
 * 
 * @param  {String} client_name    Name of the client app
 * @param  {String} remote_address Remote address of client app
 * @param  {String} pub_name       Publisher name
 * @return {String}                Data type name
 *
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.getPublishType = function (client_name, remote_address, pub_name){
	return this._getPubSubType("publish", client_name, remote_address, pub_name);
}

/**
 * Returns the type of a subscriber
 * 
 * @param  {String} client_name    Name of the client app
 * @param  {String} remote_address Remote address of client app
 * @param  {String} pub_name       Subscriber name
 * @return {String}                Data type name
 *
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.getSubscribeType = function (client_name, remote_address, sub_name){
	return this._getPubSubType("subscribe", client_name, remote_address, sub_name);
}

/**
 * Returns the type of a subscriber or publisher
 * 
 * @param  {String} pub_or_sub     Flag that identifies if matching subscriber or publisher 
 * @param  {String} client_name    Name of the client app
 * @param  {String} remote_address Remote address of client app
 * @param  {String} pub_name       Subscriber name
 * @return {String}                Data type name
 *
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin._getPubSubType = function (pub_or_sub, client_name, remote_address, pub_sub_name){
	var clients;

	for( var j = 0; j < this.admin.clients.length; j++ ){
		client = this.admin.clients[j];
		if ( client.name === client_name && client.remoteAddress === remote_address ) {
			for( var i = 0; i < client[pub_or_sub].messages.length; i++ ){
				//if (this.debug) console.log("Compare Types " + client[pub_or_sub].messages[i].name + " with " + pub_sub_name)
				if (client[pub_or_sub].messages[i].name === pub_sub_name) {
					return client[pub_or_sub].messages[i].type;
				}
			}
		}
	}
	return false;
}

/**
 * Checks if the a client name and ip address refer to current app
 * 
 * @param  {String}  client_name    Name of the client
 * @param  {String}  remote_address IP address of the client
 * @return {Boolean}                True if name and ip address refers to current app
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.isThisApp = function (client_name, remote_address){
	if (this._name === client_name && this.admin.remoteAddress === remote_address) return true;
	else return false;
}

/**
 * Returns the client that matches the name and remoteAddress parameters queried.
 * 
 * @param  {String} name           	Name of the client application
 * @param  {String} remoteAddress  	IP address of the client apps
 * @return {Object}                	Object featuring all client config information
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.getClient = function (name, remoteAddress){
	var client;

	for( var j = 0; j < this.admin.clients.length; j++ ){
		client = this.admin.clients[j];
		if ( client.name === name && client.remoteAddress === remoteAddress ) {
			return client;
		}
	}
}

/**********************************
 ** UTILITY METHODS
 **********************************/

/**
 * returns a list of all subscribers that match a specific type.
 * @param  {String} type 	Data type of subscribers that should be returned
 * @return {Array}			Array with subscribers
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.subscribeListByType = function (type){
	return this._pubSubByType("subscribe", type);
}

/**
 * returns a list of all publishers that match a specific type.
 * @param  {String} type 	Data type of publishers that should be returned
 * @return {Array}			Array with publishers
 * 
 * @memberOf Spacebrew.Admin
 * @public
 */
Spacebrew.Admin.publishListByType = function (type){
	return this._pubSubByType("publish", type);
}

/**
 * returns a list of all publishers or subscribers that match a specific type.
 * @param  {String} pub_or_sub 	Flag that identifies if method should return publishers or subscribers
 * @param  {String} type 		Data type of publishers or subscribers that should be returned
 * @return {Array}				Array with publishers
 * 
 * @memberOf Spacebrew.Admin
 * @private
 */
Spacebrew.Admin._pubSubByType = function (pub_or_sub, type){
	var client = {}
		, filtered_clients = []
		, pub_sub_item = {}
		, new_item = {}
		;

	for( var j = 0; j < this.admin.clients.length; j++ ){
		client = this.admin.clients[j];
		for (var i = 0; i < client[pub_or_sub].messages.length; i++) {
			pub_sub_item = client[pub_or_sub].messages[i];
			if ( pub_sub_item.type === type ) {
				new_item = { clientName: client.name
							, remoteAddress: client.remoteAddress 
							, name: pub_sub_item.name
							, type: pub_sub_item.type
						};
				filtered_clients.push( new_item );
			}			
		}
	}
	return filtered_clients;
}
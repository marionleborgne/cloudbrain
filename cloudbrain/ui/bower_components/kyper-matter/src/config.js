let config = {
	serverUrl: 'http://tessellate.elasticbeanstalk.com',
	tokenName: 'matter'
};
//Set server to local server if developing
if (typeof window != 'undefined' && (window.location.hostname == '' || window.location.hostname == 'localhost')) {
	config.serverUrl = 'http://localhost:4000';
}
export default config;

# Muse OSC ( from muse_io binary ) to Spacebrew Bridge
# The Ruby library for Spacebrew is very alpha but the Javascript, Python, Processing libraties are solid.
# I wrote this in Ruby because I'm primarily a Rubyist.
# This is just demo code and likely shouldn't be written in Ruby in a production environment unless a good Ruby
#  implementation of Spacebrew becomes available.

require 'ruby-osc'
require 'faye/websocket'
require 'eventmachine'
require 'json'

include OSC

EM.run do
  spacebrew = Faye::WebSocket::Client.new('ws://localhost:9000')
  
  spacebrew.on :open do |event|
    # Send our configuration when the WebSocket opens.
    config =
      {
        config: {
          name: 'muse', # Name of this publisher. Note, these do not have to be unique.
          publish: {
            # List of messages this Spacebrew client will publish.
            # This would need to be fleshed out to include everything we'd want to publish to the clients.
            messages: [
              {
                name: 'concentration',
                type: 'string'
              },
              {
                name: 'mellow',
                type: 'string'
              },
              {
                name: 'eeg',
                type: 'string'
              },
              {  
                name: 'accelerometer',
                type: 'string'
              }
            ]
          }
        }
      }

      # Register this client with Spacebrew.
    spacebrew.send JSON.generate(config)
  end  
  
  spacebrew.on :error do |event|
    p event.inspect
  end  

  # This is a small OSC server which the MuseIO dev kit will connect to.
  # OSC is based off pathes, so we're using pattern matching to extract the specific data we want.
  # The full lisf of paths is available in the MuseIO documentation
  # https://sites.google.com/a/interaxon.ca/muse-developer-site/museio/osc-paths/osc-paths---v3-6-0 
  
  OSC.run do
    osc_server = Server.new 9090
    
    # These examples below are just two of dozens of paths we can possibly match. This would be a solid
    # place for some metaprogramming, or at least something less manual.
    
    # Match the Muse concentration path
    osc_server.add_pattern %r{/muse/elements/experimental/concentration} do |*args|    
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'concentration',
            type: 'string',
            value: JSON.generate(args)
          }
        }  
      
      # Send Spacebrew the concentration data for this Muse.  
      spacebrew.send JSON.generate(publish)    
    end
    
    # Match the Muse accelerometer path
    osc_server.add_pattern %r{/muse/acc} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'accelerometer',
            type: 'string',
            value: JSON.generate(args)
          }
        }

      spacebrew.send JSON.generate(publish)
    end

    # Match the Muse eeg path
    osc_server.add_pattern %r{/muse/eeg} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'eeg',
            type: 'string',
            value: JSON.generate(args)
          }
        }

      spacebrew.send JSON.generate(publish)
    end

    # Match the Muse mellow path
    osc_server.add_pattern %r{/muse/elements/experimental/mellow} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'mellow',
            type: 'string',
            value: JSON.generate(args)
          }
        }
      
      spacebrew.send JSON.generate(publish)
    end

    # Match the Muse battery path
    osc_server.add_pattern %r{/muse/batt} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'battery',
            type: 'string',
            value: JSON.generate(args)
          }
        }
      
      spacebrew.send JSON.generate(publish)
    end

    osc_server.add_pattern %r{/muse/dsp/is_good} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'is_good',
            type: 'string',
            value: JSON.generate(args)
          }
        }
      
      spacebrew.send JSON.generate(publish)
    end

    osc_server.add_pattern %r{/muse/dsp/blink} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'blink',
            type: 'string',
            value: JSON.generate(args)
          }
        }
      
      spacebrew.send JSON.generate(publish)
    end

    osc_server.add_pattern %r{/muse/dsp/jaw_clench} do |*args|
      publish =
        {
          message: {
            clientName: 'muse',
            name: 'jaw_clench',
            type: 'string',
            value: JSON.generate(args)
          }
        }
      
      spacebrew.send JSON.generate(publish)
    end
  end
end

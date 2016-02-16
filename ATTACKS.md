# Attacks

This document recopile implemented attacks by Enteletaor.

## Specific by broker/MQ

Some attacks only can be done in specific software. Here the list of them:

## Redis

#. Poisoning cache
#. Execute remote script

## Common attacks

These attacks can be executed in all of brokers/MQ:

#. Read remote info
#. Looking for sensible information (i.e. user/password)
#. Remote command injection
#. Listing remote process
#. Reject all messages stored in queues to avoid clients to receive them

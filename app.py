#!/usr/bin/env python3

import connexion

##
## Enable SSL if necessary
##
#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('yourserver.key')
#context.use_certificate_file('yourserver.crt')

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'LUMA (Local User MApping) is a REST server that exposes simple REST API that\ncan be used to map users (of any system/kind) to storage specific user\ncredentials (e.g. UID/GID, usernames and passwords or certificates), in the\nprocess authorizing them with the storage.\n\nThis is a specification of LUMA interface, which is understood by\nOneprovider, and for each storage it is best to implement a specific LUMA\nimplementation.\n\nA stub implementation can be generated automatically from this specification\nusing [Swagger Codegen](https://github.com/swagger-api/swagger-codegen)\ntool in mulitple programming frameworks.\n\nLUMA provides a 2-way mapping interface allowing to:\n * Get user credentials for specific storage based on user federated Id\n * Get user federated Id (in specific IdP) based on storage credentials\n\nAdditionally, LUMA allows for mapping between user groups on a federated (IdP)\nlevel and storage, independently of any specific user.\n\nLUMA supports the same storage systems which are supported by Oneprovider,\nand for each of them a specific must be implemented as typically different\nstorage systems require different types of credentials.\n\nAs of now there are the following supported storage systems, each with it&#39;s\nown type of credentials:\n * Posix\n * Ceph\n * Amazon S3\n * Openstack Swift\n * GlusterFS\n\nMore information: [https://github.com/onedata/luma](https://github.com/onedata/luma)\n'})
    app.run(port=8080, debug=True,
            #ssl_context=context
            )

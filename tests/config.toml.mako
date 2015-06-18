[application.main]
use = "package:montague_testapps#basic_app"
path_info = ["${here}", "${__file__}"]
env_val = "${environ['foo']}"

[application.filtered-app]
filter-with = "filter"
use = "package:montague_testapps#basic_app"

[application.egg]
use = "egg:montague_testapps#other"

[filter.filter]
use = "egg:montague_testapps#caps"
method_to_call = "lower"

[server.server_runner]
use = "egg:montague_testapps#server_runner"
host = "127.0.0.1"

[server.server_factory]
use = "egg:montague_testapps#server_factory"
port = 42

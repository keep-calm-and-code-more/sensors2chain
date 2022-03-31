rm peer_pb2.py
curl -O https://gitee.com/BTAJL/repchain/raw/master/src/main/protobuf/peer.proto
protoc *.proto --python_out=.
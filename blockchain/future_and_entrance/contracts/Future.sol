pragma solidity >=0.4.21 <0.6.0;

contract Future {
  event FutureFlag(string server, string port);

  constructor() public {
  }

  function getFlag(uint256 _secret, string memory _server, string memory _port) public {
    require (_secret == uint256(keccak256(abi.encode(blockhash(block.number - 1)))) );
    emit FutureFlag(_server, _port);
  }
}

// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
contract Arbitration_Seller_Witness{
    int256[] public positionSend;
    int256[] public positionKeep;
    int256 public index;
    // sent fron buyer to seller,uploaded by seller
    address public seller;
    address public buyer;
    address public witness;
    constructor() payable {
        seller=msg.sender;
        //the first person call this contract is the owner
    }
    function Seller_up_send(int256[] memory send) public returns(string memory){
        require(msg.sender==seller);//only seller can call this function
        positionSend=send;
        return "Successfully upload positionSend!,remember to up load keep and buyer's address";
    }
    function Seller_up_kend(int256[] memory keep) public returns(string memory){
        require(msg.sender==seller);//only seller can call this function
        positionKeep=keep;
        return "Successfully upload positionKeep!,remember to up load send and buyer's address";
    }
    function Buyer_address(address  _a) public returns(string memory){
        require(msg.sender==seller);
        buyer=_a;
        return "Successfully upload buyer's address!,remember to up load send and keep";
    }
    function Witness_UP(int256[] memory data) public{
        require(msg.sender!=buyer);
        uint num=0;
        for(uint i=0;i<positionSend.length;i++){
            if((positionSend[i]-data[i])<10){
                num+=1;
            }
        }
        if(num>=4450){
            require(index!=1,"You are not the first witness!");
            address payable _wit=payable(msg.sender);
            _wit.transfer(1 ether);
            index=1;
            witness=msg.sender;
        }
        else{
            address payable _buyer=payable(buyer);
            _buyer.transfer(0.00000005 ether);
        }
    }
    function get_witness() public  view returns 
    (string memory, address,string memory,address ,string memory,address )
    {
        return ("witness",witness,"seller",seller,"buyer",buyer);
    }  
    fallback() external {}
    receive() payable external {}
}

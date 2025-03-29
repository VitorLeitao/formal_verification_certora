/***
 * # ERC20 Token Simple Test
 *
 * Minimal test for setName function.
 */

methods {
    function balanceOf(address) external returns(uint) envfree;  
    function name() external returns(string) envfree;
    function symbol() external returns(string) envfree;
    function decimals() external returns(uint8) envfree;
    function setName(string) external;
    function setSymbol(string) external;
    function setDecimals(uint8) external;
    function mint(address, uint256) external;
    function burn(address, uint256) external;
    
    // Métodos do ERC20
    function transfer(address, uint256) external;
    function approve(address, uint256) external;
    function transferFrom(address, address, uint256) external;
    function allowance(address, address) external returns(uint) envfree;

    // Métodos do Ownable
    function owner() external returns(address) envfree;
    function transferOwnership(address) external;
}

/// Mint must add `amount` tokens to `recipient`
rule mintSpec {
    address owner; address recip; uint amount;

    env e;
    require e.msg.sender == owner; // Somente o proprietário pode cunhar tokens

    mathint balance_recip_before = balanceOf(recip);

    mint(e, recip, amount);

    mathint balance_recip_after = balanceOf(recip);

    assert balance_recip_after == balance_recip_before + amount,
        "mint must increase recipient's balance by amount";
}

/// Mint must add `amount` tokens to `recipient`
rule mintSpecTeste {
    address owner; 
    address recip; 
    uint amount;

    env e;
    require e.msg.sender == owner; // Somente o proprietário pode cunhar tokens

    uint balance_recip_before = balanceOf(recip);

    mint(e, recip, amount);

    uint balance_recip_after = balanceOf(recip);

    assert balance_recip_after == balance_recip_before + amount,
        "mint must increase recipient's balance by amount";
}


/// Burn must remove `amount` tokens from `account`
rule burnSpec {
    address owner; address account; uint amount;

    env e;
    require e.msg.sender == owner; // Somente o proprietário pode queimar tokens

    mathint balance_account_before = balanceOf(account);

    burn(e, account, amount);

    mathint balance_account_after = balanceOf(account);

    assert balance_account_after == balance_account_before - amount,
        "burn must decrease account's balance by amount";
}


/// setDecimals must change the token decimals (only once)
rule setDecimalsSpec {
    address owner; 
    uint8 newDecimals;

    env e;
    require e.msg.sender == owner; // Apenas o proprietário pode alterar os decimais

    uint8 decimals_before = decimals();

    setDecimals(e, newDecimals);

    uint8 decimals_after = decimals();

    assert decimals_after == newDecimals, 
        "setDecimals must change the token decimals";
}


/// setSymbol must change the token symbol
rule setSymbolSpec {
    address owner; 
    string newSymbol;

    env e;
    require e.msg.sender == owner; // Apenas o proprietário pode alterar o símbolo

    string symbol_before = symbol();

    setSymbol(e, newSymbol);

    string symbol_after = symbol();

    assert symbol_after == newSymbol, 
        "setSymbol must change the token symbol";
}



// COMPLEMENTARES

/// transferOwnership must change the contract owner
rule transferOwnershipSpec {
    address currentOwner;
    address newOwner;

    env e;
    require e.msg.sender == currentOwner; // Somente o dono pode transferir a propriedade

    address owner_before = owner();

    transferOwnership(e, newOwner);

    address owner_after = owner();

    assert owner_after == newOwner, 
        "transferOwnership must change contract owner";
}


/// approve must set the allowance correctly
rule approveSpec {
    address owner;
    address spender;
    uint amount;

    env e;
    require e.msg.sender == owner; // Apenas o dono da conta pode aprovar

    uint allowance_before = allowance(owner, spender);

    approve(e, spender, amount);

    uint allowance_after = allowance(owner, spender);

    assert allowance_after == amount, 
        "approve must set the correct allowance";
}

/// transferFrom must transfer allowed tokens from one account to another
rule transferFromSpec {
    address owner;
    address spender;
    address recipient;
    uint amount;

    env e;
    require e.msg.sender == spender; // Apenas o `spender` pode transferir
    approve(e, spender, amount); // Primeiro, precisamos aprovar a transferência

    uint balance_owner_before = balanceOf(owner);
    uint balance_recipient_before = balanceOf(recipient);

    transferFrom(e, owner, recipient, amount);

    uint balance_owner_after = balanceOf(owner);
    uint balance_recipient_after = balanceOf(recipient);

    assert balance_owner_after == balance_owner_before - amount,
        "transferFrom must decrease sender's balance";
    assert balance_recipient_after == balance_recipient_before + amount,
        "transferFrom must increase recipient's balance";
}

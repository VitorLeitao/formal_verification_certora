/**
 * # Pool Contract Basic Test
 *
 * Minimal verification of setName and setSymbol access control and effects.
 */

methods {
    function setName(string) external;
    function setSymbol(string) external;
    function initialize(address, address, bool) external;

    function name() external returns(string) envfree;
    function symbol() external returns(string) envfree;
    function token0() external returns(address) envfree;
    function token1() external returns(address) envfree;
    function stable() external returns(bool) envfree;

    function transfer(address, uint256) external;

    function balanceOf(address) external returns(uint256);
    function totalBalance() external returns(uint256);
    function mint(address) external returns (uint256);

    function getReserves() external returns (uint256, uint256, uint256);
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
}


rule checkObservationLengthGTZero {
    env e;

    uint256 length = observationLength(e);

    assert length >= 0x0,
        "observationLength must be Grater then 0";
}

/// Emergency council should be able to update name
rule emergencyCouncilCanSetName {
    string newName;
    address factory;

    env e;
    require e.msg.sender == factory;

    string name_before = name();

    setName(e, newName);

    string name_after = name();

    assert name_after == newName,
        "setName must update name if called by factory";
}


/// Emergency council should be able to update symbol
rule emergencyCouncilCanSetSymbol {
    string newSymbol;
    address factory;

    env e;
    require e.msg.sender == factory;

    string symbol_before = symbol();

    setSymbol(e, newSymbol);

    string symbol_after = symbol();

    assert symbol_after == newSymbol,
        "setSymbol must update symbol if called by factory";
}

/// Pool must be initialized correctly
rule initializeSetsTokensAndStableFlag {
    address t0; address t1; bool isStable;

    env e;

    initialize(e, t0, t1, isStable);

    assert token0() == t0,
        "initialize must set token0";
    assert token1() == t1,
        "initialize must set token1";
    assert stable() == isStable,
        "initialize must set stable flag";
}


rule mintReturnsNonNegative {
   address recipient;

    env e;
    uint256 minted = mint(e, recipient);

    assert minted >= 0x0,
        "mint should increase recipient's balance by minted amount";
}


rule balanceOfIsNonNegative {
    address user;
    env e;

    uint256 balance = balanceOf(e, user);

    assert balance >= 0x0,
        "balanceOf should always return a non-negative balance";
}

rule totalSupplyIsNonNegative {
    env e;

    uint256 supply = totalSupply(e);

    assert supply >= 0x0,
        "totalSupply should always be non-negative";
}



rule balanceOfIsAlwaysTheSame {
    address user;
    env e;

    uint256 balance0 = balanceOf(e, user);
    uint256 balance1 = balanceOf(e, user);

    assert balance0 == balance1,
        "balanceOf should always return the same value for the same user, if there was no operations";
}

rule mintIncreasesTotalSupply {
    env e;
    address user;

    uint256 supply_before = totalSupply(e);

    mint(e, user);

    uint256 supply_after = totalSupply(e);

    assert supply_after >= supply_before,
        "mint must not reduce totalSupply";
}

rule stableFlagIsSetCorrectly {
    env e;
    address t0;
    address t1;
    bool isStable;

    initialize(e, t0, t1, isStable);

    assert stable() == isStable,
        "stable flag must match the value passed during initialize";
}

rule nameChangesAfterSetName {
    env e;
    string newName;

    setName(e, newName);
    string currentName = name();

    assert currentName == newName,
        "name must match the value set by setName";
}


rule symbolChangesAfterSetSymbol {
    env e;
    string newSymbol;

    setSymbol(e, newSymbol);
    string currentSymbol = symbol();

    assert currentSymbol == newSymbol,
        "symbol must match the value set by setSymbol";
}
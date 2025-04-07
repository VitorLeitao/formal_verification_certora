methods {
    // Declaração da função de inicialização
    function initialize(address, address, bool) external;
    
    // Declaração da função metadata (os retornos serão capturados via acesso indexado)
    function metadata() external view;
}

rule metadataTest {
    // Variáveis simbólicas para os parâmetros de initialize
    address tokenA;
    address tokenB;
    bool isStable;
    env e;
    
    // Chama initialize para configurar o pool
    initialize(tokenA, tokenB, isStable);
    
    // Chama metadata e captura os retornos numa tupla
    // Os elementos retornados são, na ordem:
    // [0]: dec0, [1]: dec1, [2]: reserve0, [3]: reserve1, [4]: stable, [5]: token0, [6]: token1
    let ret := metadata();
    
    // Como não houve depósitos, as reservas devem ser zero
    assert ret[2] == 0;
    assert ret[3] == 0;
    
    // O flag de pool (stable) deve ser igual ao parâmetro isStable passado
    assert ret[4] == isStable;
    
    // Os tokens retornados devem ser os mesmos passados na inicialização
    assert ret[5] == tokenA;
    assert ret[6] == tokenB;
}

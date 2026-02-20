/**
 * Simple Agent Spawner - Minimal Example
 * 
 * This is the simplest possible demonstration of spawning
 * a sub-agent with a custom name and model.
 */

async function simpleSpawnExample() {
    // Spawn a helper agent with specific configuration
    const helper = await spawnAgent({
        name: "math-helper",
        model: "nvidia-nim/moonshotai/kimi-k2.5",
        task: "Calculate 2 + 2 and explain your reasoning"
    });
    
    console.log(`Spawned agent: ${helper.name}`);
    console.log(`Agent ID: ${helper.id}`);
    
    return helper;
}

// Example of spawning multiple agents with different models
async function multiModelExample() {
    const agents = [
        { name: "fast-helper", model: "nvidia-nim/moonshotai/kimi-k2.5", task: "Quick summary" },
        { name: "deep-thinker", model: "nvidia-nim/moonshotai/kimi-k2.5", task: "Deep analysis" },
        { name: "creative-bot", model: "nvidia-nim/moonshotai/kimi-k2.5", task: "Be creative" }
    ];
    
    const spawned = [];
    for (const config of agents) {
        const agent = await spawnAgent(config);
        spawned.push(agent);
        console.log(`✅ Spawned ${config.name} using ${config.model}`);
    }
    
    return spawned;
}

module.exports = { simpleSpawnExample, multiModelExample };

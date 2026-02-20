#!/usr/bin/env node
/**
 * Example Sub-Agent: Multi-Model Demonstration
 * 
 * This sub-agent demonstrates how to spawn additional agents with:
 * - Different names/identities
 * - Different AI models
 * - Different specializations
 */

const { spawnAgent } = require('openclaw');

async function main() {
    console.log("🤖 Multi-Model Agent Spawner Demo");
    console.log("==================================\n");

    // Define different agent configurations to demonstrate variety
    const agentConfigs = [
        {
            name: "code-reviewer",
            model: "nvidia-nim/moonshotai/kimi-k2.5",
            description: "Specialized code reviewer focused on best practices",
            task: "Review the following code for bugs and suggest improvements:\n\nfunction add(a, b) {\n  return a + b;\n}"
        },
        {
            name: "creative-writer", 
            model: "nvidia-nim/moonshotai/kimi-k2.5",
            description: "Creative writing assistant with a poetic style",
            task: "Write a haiku about artificial intelligence"
        },
        {
            name: "data-analyzer",
            model: "nvidia-nim/moonshotai/kimi-k2.5",
            description: "Data analysis specialist focused on insights",
            task: "Analyze this dataset: [10, 25, 30, 45, 50, 65, 80]. Calculate mean, median, and suggest what this trend might indicate."
        }
    ];

    console.log(`Spawning ${agentConfigs.length} specialized agents...\n`);

    const results = [];

    for (const config of agentConfigs) {
        console.log(`📤 Spawning: ${config.name}`);
        console.log(`   Model: ${config.model}`);
        console.log(`   Role: ${config.description}`);
        
        try {
            // Spawn the sub-agent with specific configuration
            const agent = await spawnAgent({
                name: config.name,
                model: config.model,
                task: config.task,
                timeout: 60000, // 60 second timeout
                metadata: {
                    description: config.description,
                    spawnedAt: new Date().toISOString()
                }
            });

            console.log(`   ✅ Agent spawned successfully (ID: ${agent.id})`);
            results.push({ name: config.name, status: 'success', agentId: agent.id });
            
        } catch (error) {
            console.log(`   ❌ Failed to spawn: ${error.message}`);
            results.push({ name: config.name, status: 'error', error: error.message });
        }
        
        console.log();
    }

    // Summary
    console.log("\n📊 Spawn Summary");
    console.log("================");
    const successful = results.filter(r => r.status === 'success').length;
    const failed = results.filter(r => r.status === 'error').length;
    
    console.log(`Total agents: ${results.length}`);
    console.log(`Successful: ${successful} ✅`);
    console.log(`Failed: ${failed} ❌`);
    
    console.log("\n📝 Agent Details:");
    results.forEach(r => {
        const icon = r.status === 'success' ? '✅' : '❌';
        console.log(`  ${icon} ${r.name}: ${r.status}`);
        if (r.agentId) {
            console.log(`     ID: ${r.agentId}`);
        }
    });

    return { success: successful > 0, results };
}

// Run if called directly
if (require.main === module) {
    main()
        .then(result => {
            console.log("\n✨ Demo complete!");
            process.exit(result.success ? 0 : 1);
        })
        .catch(err => {
            console.error("\n💥 Demo failed:", err);
            process.exit(1);
        });
}

module.exports = { main };

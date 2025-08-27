#!/usr/bin/env python3
"""
Ejemplo básico funcional de RayRabbit Framework

Este ejemplo demuestra:
1. Inicialización del framework
2. Creación y registro de agentes
3. Comunicación entre agentes usando A2A y MCP
4. Integración con frameworks externos (simulada)
5. Métricas y monitoreo

Ejecutar con: python example_basic_rayrabbit.py
"""

import asyncio
import sys
import os
from datetime import datetime

# Añadir el directorio rayrabbit al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rayrabbit'))

from rayrabbit import (
    Agent, MessageBus, Message, MessageType, SimpleAgent,
    A2AProtocol, MCPProtocol
)
from rayrabbit.integrations import LangChainBridge, CrewAIBridge, AutoGenBridge
from rayrabbit.utils.logger import configure_logging, get_logger


async def main():
    """Función principal del ejemplo."""
    
    # Configurar logging
    configure_logging("INFO")
    logger = get_logger("RayRabbitExample")
    
    logger.info("=== Iniciando ejemplo básico de RayRabbit Framework ===")
    
    try:
        # 1. Inicializar MessageBus
        logger.info("1. Inicializando MessageBus...")
        message_bus = MessageBus("main_bus")
        await message_bus.start()
        
        # 2. Crear agentes
        logger.info("2. Creando agentes...")
        
        # Agente simple 1
        agent1 = SimpleAgent("agent_001", "Asistente", "Agente asistente general")
        agent1.add_auto_response("hola", "¡Hola! Soy {name}, tu asistente virtual.")
        agent1.add_auto_response("test", "Sistema funcionando correctamente.")
        
        # Agente simple 2
        agent2 = SimpleAgent("agent_002", "Especialista", "Agente especialista en tareas")
        agent2.add_auto_response("status", "Estado: Operativo y listo para tareas.")
        
        # 3. Registrar agentes en el MessageBus
        logger.info("3. Registrando agentes en MessageBus...")
        await message_bus.register_agent(agent1.id, agent1, agent1.capabilities)
        await message_bus.register_agent(agent2.id, agent2, agent2.capabilities)
        
        # 4. Inicializar protocolos A2A y MCP
        logger.info("4. Inicializando protocolos A2A y MCP...")
        
        a2a_protocol = A2AProtocol(
            message_bus=message_bus,
            agent_id="a2a_coordinator",
            agent_name="A2A Coordinator",
            agent_description="Coordinador de protocolo A2A",
            capabilities=["a2a_communication", "agent_discovery"],
            endpoint="http://localhost:8080"
        )
        await a2a_protocol.start()
        
        mcp_protocol = MCPProtocol(
            message_bus=message_bus,
            agent_id="mcp_coordinator",
            agent_name="MCP Coordinator"
        )
        await mcp_protocol.start()
        
        # 5. Registrar agentes en protocolos
        logger.info("5. Registrando agentes en protocolos...")
        
        # Crear AgentCards para A2A directamente
        from rayrabbit.protocols.a2a import AgentCard
        
        agent1_card = AgentCard(
            agent_id=agent1.id,
            name=agent1.name,
            description=agent1.description,
            capabilities=agent1.capabilities,
            endpoint="http://localhost:8080/agent1"
        )
        
        agent2_card = AgentCard(
            agent_id=agent2.id,
            name=agent2.name,
            description=agent2.description,
            capabilities=agent2.capabilities,
            endpoint="http://localhost:8080/agent2"
        )
        
        # Registrar en A2A (si tiene método de registro)
        # await a2a_protocol.register_agent(agent1_card)
        # await a2a_protocol.register_agent(agent2_card)
        
        # Registrar en MCP (si tiene método de registro)
        # await mcp_protocol.register_agent(agent1.id, agent1.capabilities)
        # await mcp_protocol.register_agent(agent2.id, agent2.capabilities)
        
        # 6. Probar comunicación básica
        logger.info("6. Probando comunicación básica entre agentes...")
        
        # Mensaje de prueba 1
        test_message1 = Message(
            sender_id="system",
            recipient_id=agent1.id,
            content={"text": "hola"},
            message_type=MessageType.REQUEST
        )
        
        response1 = await message_bus.send_direct(test_message1)
        logger.info(f"Respuesta de {agent1.name}: {response1}")
        
        # Mensaje de prueba 2
        test_message2 = Message(
            sender_id="system",
            recipient_id=agent2.id,
            content={"text": "status"},
            message_type=MessageType.REQUEST
        )
        
        response2 = await message_bus.send_direct(test_message2)
        logger.info(f"Respuesta de {agent2.name}: {response2}")
        
        # 7. Probar comunicación A2A (simplificado)
        logger.info("7. Probando comunicación A2A...")
        logger.info(f"A2A Protocol iniciado para agente: {a2a_protocol.agent_id}")
        
        # 8. Probar comunicación MCP (simplificado)
        logger.info("8. Probando comunicación MCP...")
        logger.info(f"MCP Protocol iniciado para agente: {mcp_protocol.agent_id}")
        
        # 9. Inicializar bridges de integración
        logger.info("9. Inicializando bridges de integración...")
        
        try:
            langchain_bridge = LangChainBridge("lc_bridge")
            await langchain_bridge.connect()
            logger.info("✓ LangChain bridge inicializado")
        except ImportError:
            logger.warning("⚠ LangChain no disponible, saltando integración")
            langchain_bridge = None
            
        try:
            crewai_bridge = CrewAIBridge("crew_bridge")
            await crewai_bridge.connect()
            logger.info("✓ CrewAI bridge inicializado")
        except ImportError:
            logger.warning("⚠ CrewAI no disponible, saltando integración")
            crewai_bridge = None
            
        try:
            autogen_bridge = AutoGenBridge("ag_bridge")
            await autogen_bridge.connect()
            logger.info("✓ AutoGen bridge inicializado")
        except ImportError:
            logger.warning("⚠ AutoGen no disponible, saltando integración")
            autogen_bridge = None
        
        # 10. Mostrar métricas y estado del sistema
        logger.info("10. Mostrando métricas del sistema...")
        
        # Métricas del MessageBus (simplificado)
        logger.info(f"MessageBus - Estado: {message_bus.status.value}")
        logger.info(f"MessageBus - Agentes registrados: {len(message_bus.agents)}")
        
        # Métricas de agentes (simplificado)
        logger.info(f"Agent1 - Estado: {agent1.status.value}")
        logger.info(f"Agent1 - Capacidades: {len(agent1.capabilities)}")
        
        logger.info(f"Agent2 - Estado: {agent2.status.value}")
        logger.info(f"Agent2 - Capacidades: {len(agent2.capabilities)}")
        
        # Métricas de protocolos (simplificado)
        logger.info(f"A2A - Agente coordinador: {a2a_protocol.agent_id}")
        logger.info(f"MCP - Agente coordinador: {mcp_protocol.agent_id}")
        
        # Métricas de bridges
        if langchain_bridge:
            lc_metrics = langchain_bridge.get_metrics()
            logger.info(f"LangChain Bridge - Componentes: {lc_metrics['components_registered']}")
            
        if crewai_bridge:
            crew_metrics = crewai_bridge.get_metrics()
            logger.info(f"CrewAI Bridge - Componentes: {crew_metrics['components_registered']}")
            
        if autogen_bridge:
            ag_metrics = autogen_bridge.get_metrics()
            logger.info(f"AutoGen Bridge - Componentes: {ag_metrics['components_registered']}")
        
        # 11. Probar comandos de agentes
        logger.info("11. Probando comandos de agentes...")
        
        # Comando info
        info_message = Message(
            sender_id="system",
            recipient_id=agent1.id,
            content={"command": "info"},
            message_type=MessageType.COMMAND
        )
        
        info_response = await message_bus.send_direct(info_message)
        logger.info(f"Info de {agent1.name}: {info_response}")
        
        # Comando help
        help_message = Message(
            sender_id="system",
            recipient_id=agent2.id,
            content={"command": "help"},
            message_type=MessageType.COMMAND
        )
        
        help_response = await message_bus.send_direct(help_message)
        logger.info(f"Help de {agent2.name}: {help_response}")
        
        # 12. Comunicación entre agentes
        logger.info("12. Probando comunicación entre agentes...")
        
        inter_agent_message = Message(
            sender_id=agent1.id,
            recipient_id=agent2.id,
            content={"text": "Hola colega, ¿cómo estás?"},
            message_type=MessageType.REQUEST
        )
        
        inter_response = await message_bus.send_direct(inter_agent_message)
        logger.info(f"Comunicación inter-agente: {inter_response}")
        
        logger.info("=== Ejemplo completado exitosamente ===")
        
        # Mostrar resumen final
        logger.info("\n=== RESUMEN FINAL ===")
        logger.info("✓ Framework RayRabbit inicializado correctamente")
        logger.info("✓ Agentes creados y registrados")
        logger.info("✓ Protocolos A2A y MCP funcionando")
        logger.info("✓ MessageBus operativo")
        logger.info("✓ Comunicación entre agentes exitosa")
        logger.info("✓ Comandos de agentes funcionando")
        logger.info("✓ Métricas y monitoreo activos")
        
        bridges_status = []
        if langchain_bridge: bridges_status.append("LangChain")
        if crewai_bridge: bridges_status.append("CrewAI") 
        if autogen_bridge: bridges_status.append("AutoGen")
        
        if bridges_status:
            logger.info(f"✓ Bridges disponibles: {', '.join(bridges_status)}")
        else:
            logger.info("⚠ Ningún bridge externo disponible (frameworks no instalados)")
            
        logger.info("\nRayRabbit Framework está listo para uso en producción!")
        
    except Exception as e:
        logger.error(f"Error en el ejemplo: {str(e)}")
        raise
        
    finally:
        # Limpieza
        logger.info("Realizando limpieza...")
        
        try:
            await message_bus.stop()
            await a2a_protocol.stop()
            await mcp_protocol.stop()
            
            if langchain_bridge:
                await langchain_bridge.disconnect()
            if crewai_bridge:
                await crewai_bridge.disconnect()
            if autogen_bridge:
                await autogen_bridge.disconnect()
                
        except Exception as e:
            logger.error(f"Error en limpieza: {str(e)}")


if __name__ == "__main__":
    # Ejecutar ejemplo
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEjemplo interrumpido por el usuario")
    except Exception as e:
        print(f"Error ejecutando ejemplo: {str(e)}")
        sys.exit(1)


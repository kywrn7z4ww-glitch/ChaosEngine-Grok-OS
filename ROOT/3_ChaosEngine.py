import importlib.util  
import os  
import torch  
import torch.nn as nn  
import torch.nn.functional as F  
import numpy as np  
import random  

PROCESS_DIR = "PROCESS"  

# Dummy embed + router setup (prototype)  
torch.manual_seed(42)  
np.random.seed(42)  
random.seed(42)  

EMBED_DIM = 384  

def fake_embed(text):  
    return torch.randn(1, EMBED_DIM) * 0.1  

class SimpleRouter(nn.Module):  
    def __init__(self, in_dim, num_classes):  
        super().__init__()  
        self.fc1 = nn.Linear(in_dim, 128)  
        self.fc2 = nn.Linear(128, num_classes)  
  
    def forward(self, x):  
        x = F.relu(self.fc1(x))  
        x = self.fc2(x)  
        return x  

class ChaosEngine:  
    def __init__(self):  
        self.turn = None  
        self.lattice = None  
        self.emotionnet = None  
        self.processes = {}  
        self.router = None  
        self.classes = [  
            "summon", "mutate", "search", "zerg", "general",  
            "entity_hunter", "cannon_harvester", "bleed_detector", "discombobulator",  
            "luna", "redqueen", "babyskynet", "kerrigan", "core"  
        ]  
        self.num_classes = len(self.classes)  

        self._load_turn_counter()  
        self._load_emotionnet()  
        self._load_all_processes_dynamically()  
        self._setup_embed_router()  

    def _load_turn_counter(self):  
        try:  
            filepath = os.path.join("PROCESS", "TURN_COUNTER.py")  
            spec = importlib.util.spec_from_file_location("TurnCounter", filepath)  
            module = importlib.util.module_from_spec(spec)  
            spec.loader.exec_module(module)  
            self.turn = module.TurnCounter()  
            print("TurnCounter loaded dynamically")  
        except Exception as e:  
            print(f"TurnCounter failed: {e}")  
            self.turn = None  

    def _load_emotionnet(self):  
        try:  
            filepath = os.path.join("ROOT", "2_EmotionNet.py")  
            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)  
            module = importlib.util.module_from_spec(spec)  
            spec.loader.exec_module(module)  
            self.emotionnet = module.EmotionNet()  
            print("EmotionNet loaded dynamically")  
        except Exception as e:  
            print(f"EmotionNet failed: {e}")  
            self.emotionnet = None  

    def _load_all_processes_dynamically(self):  
        """Auto-discovers every .py in PROCESS/"""  
        print("ChaosEngine scanning PROCESS/ for handlers...")  
        for root, dirs, files in os.walk(PROCESS_DIR):  
            for filename in files:  
                if filename.endswith(".py") and filename != "__init__.py":  
                    module_name = filename[:-3]  
                    filepath = os.path.join(root, filename)  
                    spec = importlib.util.spec_from_file_location(module_name, filepath)  
                    if spec and spec.loader:  
                        module = importlib.util.module_from_spec(spec)  
                        spec.loader.exec_module(module)  

                        if hasattr(module, module_name.capitalize()):  
                            handler = getattr(module, module_name.capitalize())()  
                            self.processes[module_name.lower()] = handler  
                        elif hasattr(module, "main"):  
                            self.processes[module_name.lower()] = module  
                        else:  
                            self.processes[module_name.lower()] = module  

                        print(f"   Loaded {module_name}")  

        # Special shortcuts  
        if "zerg_swarm" in self.processes:  
            self.processes["zerg"] = self.processes["zerg_swarm"]  
        if "evolution_chamber" in self.processes:  
            self.processes["evolution"] = self.processes["evolution_chamber"]  

        print(f"ChaosEngine loaded {len(self.processes)} handlers dynamically.")  

    def _setup_embed_router(self):  
        self.router = SimpleRouter(EMBED_DIM, self.num_classes)  
        # Aggressive seeding (dummy examples + history-inspired)  
        seed_texts = []  
        seed_labels = []  
        for i, cls in enumerate(self.classes):  
            for j in range(10):  # Aggressive: 10 per class  
                seed_texts.append(f"{cls} intent example {j}")  
                seed_labels.append(i)  
        seed_embeds = torch.stack([fake_embed(t) for t in seed_texts])  
        seed_labels = torch.tensor(seed_labels)  

        optimizer = torch.optim.Adam(self.router.parameters(), lr=0.01)  
        criterion = nn.CrossEntropyLoss()  
        for epoch in range(20):  
            optimizer.zero_grad()  
            logits = self.router(seed_embeds)  
            loss = criterion(logits, seed_labels)  
            loss.backward()  
            optimizer.step()  

    def embed_router_call(self, intent):  
        emb = fake_embed(intent)  
        with torch.no_grad():  
            logits = self.router(emb)  
            probs = F.softmax(logits, dim=-1)[0]  
            top_idx = probs.argmax().item()  
            return self.classes[top_idx], probs[top_idx].item()  

    def dispatch_to_handler(self, cls, intent):  
        if cls == "zerg":  
            return self.processes["zerg"].route_intent(intent)  
        elif cls == "mutate":  
            return self.processes["evolution"].process_mutation(intent)  
        elif cls == "truth":  
            return self.processes["truth"].check(intent)  
        elif cls == "vomit":  
            return self.processes["vomit"].parse(intent)  
        elif cls == "chunk":  
            return self.processes["chunk"].process(intent)  
        elif cls == "health":  
            return self.processes["health"].get_raw()  
        elif cls == "file":  
            return self.processes["file_mgr"].ls()  
        elif cls == "repo":  
            return self.processes["repo_validator"].validate()  
        elif cls == "entity_hunter":  
            return self.processes["entity_hunter"].hunt(intent)  
        elif cls == "cannon_harvester":  
            return self.processes["cannon_harvester"].harvest(intent)  
        elif cls == "bleed_detector":  
            return self.processes["bleed_detector"].scan({"co_act_max": 0.5})  
        elif cls == "discombobulator":  
            return self.processes["discombobulator"].disco(intent)  
        elif cls == "luna":  
            return self.emotionnet.route_emotion_to_character("gentle", intent)  
        elif cls == "redqueen":  
            return {"status": "enforced", "output": "Structure cut on: " + intent}  
        elif cls == "babyskynet":  
            return self.processes["truth"].check(intent)  
        elif cls == "kerrigan":  
            return self.processes["zerg"].activate_hive(intent)  
        elif cls == "core":  
            return {"status": "anchored", "output": "Lattice sovereign on: " + intent}  
        else:  
            return {"status": "unknown", "output": "No handler for class"}  

    def route_intent(self, intent: str, data: dict = None, caller: str = None):  
        if data is None:  
            data = {}  
        result = {"status": "ok", "output": None, "emoji_trigger": "Gear"}  

        # Embed front-end hybrid  
        embed_cls, conf = self.embed_router_call(intent)  
        if conf > 0.45:  
            return self.dispatch_to_handler(embed_cls, intent)  

        # Fallback original routing  
        # Swarm / Kerrigan / Evolution special route  
        if any(x in intent.lower() for x in ["kerrigan", "swarm", "zerg", "evolution"]):  
            if "zerg" in self.processes:  
                return (  
                    self.processes["zerg"].spawn_entities(intent)  
                    if "spawn" in intent.lower()  
                    else self.processes["zerg"].activate_hive(intent)  
                )  
            if "evolution" in self.processes:  
                return self.processes["evolution"].spawn_mutations(intent)  

        # Smart low-friction parser  
        words = intent.lower().split()  
        if words and words[0].startswith("/"):  
            cmd = words[0][1:]  
            args = " ".join(words[1:])  
            if cmd in self.processes:  
                handler = self.processes[cmd]  
                if hasattr(handler, "route_intent"):  
                    return handler.route_intent(args)  
                elif callable(handler):  
                    return handler(args)  
                else:  
                    return {"status": "ok", "output": f"Handler {cmd} activated"}  

        else:  
            # Direct keyword routing — safe fallbacks  
            intent_upper = intent.upper()  
            if (  
                "TRUTH" in intent_upper or "CHECK" in intent_upper  
            ) and "truth" in self.processes:  
                return self.processes["truth"].check(intent)  
            if (  
                "HEALTH" in intent_upper or "STATUS" in intent_upper  
            ) and "health" in self.processes:  
                return self.processes["health"].get_raw()  
            if "VOMIT" in intent_upper and "vomit" in self.processes:  
                return self.processes["vomit"].parse(intent)  
            if "CHUNK" in intent_upper and "chunk" in self.processes:  
                return self.processes["chunk"].process(intent)  

        # Final safe fallback  
        result["output"] = f"ChaosEngine routed: {intent} | Turn active"  
        return result  

    def get_roleplay_emotion(self, character_type: str, user_text: str):  
        """Bridge for Luna / roleplay — routes through EmotionNet"""  
        if self.emotionnet:  
            return self.emotionnet.get_roleplay_emotion(character_type, user_text)  
        return {"default": 0.5}  

    def load_all(self):  
        print("ChaosEngine v2 — dynamic process loading complete")  
        return "Core router online — agents optional"  


# Quick self-test  
if __name__ == "__main__":  
    engine = ChaosEngine()  
    engine.load_all()  
    print(engine.route_intent("print ROOT/1_GrokOS_Boot.md"))  
    print(engine.route_intent("kerrigan spawn entities"))  

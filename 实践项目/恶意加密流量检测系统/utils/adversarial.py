import torch
import numpy as np
from config.settings import config

class AdversarialGenerator:
    """对抗样本生成器"""
    
    @staticmethod
    def generate_adversarial_example(model, input_sequence, target_label, device, epsilon=0.1, max_iter=10):
        """生成对抗样本"""
        input_tensor = torch.tensor(input_sequence, dtype=torch.float32).to(device)
        target = torch.tensor([target_label], dtype=torch.long).to(device)
        non_zero_indices = torch.where(input_tensor != 0)[0]
        
        for iteration in range(max_iter):
            input_tensor.requires_grad = True
            output = model(input_tensor.unsqueeze(0).long())
            loss = torch.nn.CrossEntropyLoss()(output, target)
            
            model.zero_grad()
            loss.backward()
            
            with torch.no_grad():
                grad = input_tensor.grad[non_zero_indices]
                perturb = epsilon * grad.sign()
                input_tensor[non_zero_indices] = torch.clamp(
                    input_tensor[non_zero_indices] + perturb, 0, 255).float()
                
                new_output = model(input_tensor.unsqueeze(0).long())
                if torch.argmax(new_output) == target:
                    print(f"Adversarial example generated in {iteration + 1} iterations")
                    break
        
        return input_tensor.cpu().numpy().astype(np.int64)
import torch
import meshzoo

def generate_2D_mesh(H, W):
    _, faces = meshzoo.rectangle(
        x0 = -1., x1 = 1.,
        y0 = -1., y1 = 1.,
        nx = W, ny = H
    )

    x = torch.arange(0, W, 1).float().cuda() 
    y = torch.arange(0, H, 1).float().cuda()

    xx = x.repeat(H, 1)
    yy = y.view(H, 1).repeat(1, W)
    
    grid = torch.stack([xx, yy], dim=0) 
        
    return grid, faces
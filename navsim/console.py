import pygame

class Console(object):
    
    def __init__(self,config, show = True):
        self.config = config
        self.bg_col = pygame.Color(config['console_bg'] if 'console_bg' in config else 'grey')
        self.fg_col = pygame.Color(config['console_fg'] if 'console_fg' in config else 'black')
    
        self.rect = pygame.Rect(config['console_rect'])
        height = self.rect.height
        
        f = config['console_font'] if 'console_font' in config else ('consolas',16)
        self.font = pygame.font.SysFont(f[0],f[1])
        
        self._inc_size = f[1]
        
        self._lines = int(height / (self._inc_size+1))
        
        self.show = show
        
        self.lines = []
        config['console'] = self 
        
        pass
    
    def draw(self,surface):
        if not self.show:
            return
        rend_list = []
        
        s = pygame.Surface((self.rect.size))
        s.set_alpha(128)
        s.fill(self.bg_col)
        
        #rect = pygame.draw.rect(surface,self.bg_col,self.rect)
        rel_pos = 0
        for line in self.lines[-self._lines:]:
            tex = self.font.render(line,True,self.fg_col)
            s.blit(tex,(self.rect[0],self.rect[1] + rel_pos))
            rel_pos = rel_pos + self._inc_size
        
        surface.blit(s,self.rect.topleft)
        
    def toggle(self):
        self.show = not self.show

    def write(self,string):
        self.lines.append(string)
        self.lines = self.lines[-self._lines:]
        pass
    
    
def draw(self):
    x11 = 40 - 5 * math.sin(self.an)
    y11 = 450 + 5 * math.cos(self.an)
    x12 = 40 + 5 * math.sin(self.an)
    y12 = 450 - 5 * math.cos(self.an)

    x21 = 40 + 30 * math.cos(self.an) - 5 * math.sin(self.an)
    y21 = 450 - 30 * math.sin(self.an) + 5 * math.sin(self.an)
    x22 = 40 + 30 * math.cos(self.an) + 5 * math.sin(self.an)
    y22 = 450 + 30 * math.sin(self.an) - 5 * math.sin(self.an)
    pygame.draw.polygon(self.screen, (255, 255, 0), [[x11, y11], [x12, y12], [x21, y21], [x22, y22]])


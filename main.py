import pyglet
from pyglet.image import Animation
from pyglet.gl import GL_LINES
import random


movement_direction = 0
enemy_movement_direction = 1
enemy_speed = 0.1
enemy_bullets = []
game_over = False

#create a function to handle the enemy ships firing bullets
def fire_bullets(dt):
    global enemy_bullets, game_over_label
    #iterate through the enemies
    for enemy in enemies_sprites:
        #randomly decide if the enemy should fire a bullet
        if random.randint(1, 100) <= 2:
            #create a bullet
            bullet = pyglet.shapes.Rectangle(enemy.x, enemy.y, 5, 10, color=(0, 255, 0))
            #add the bullet to the list of enemy bullets
            enemy_bullets.append(bullet)


def check_collision(dt):
    global game_over,enemy_bullets,enemies_sprites,movement_direction,spaceship_sprite
    for bullet in enemy_bullets:
        if ((bullet.x > (spaceship_sprite.x - 25)) and (bullet.x < (spaceship_sprite.x + 25))) and (bullet.y < spaceship_sprite.y + 25 and bullet.y > spaceship_sprite.y - 25):
            
            game_over = True
            print("Game Over")
            pyglet.clock.unschedule(check_collision)
            game_window.pop_handlers()
            game_over_label.visible = True
            



def on_key_release(symbol, modifiers):
    global movement_direction
    if symbol in (pyglet.window.key.LEFT, pyglet.window.key.RIGHT):
        movement_direction = 0

def on_key_press(symbol, modifiers):
    global movement_direction
    if symbol == pyglet.window.key.LEFT:
        movement_direction = -1
    elif symbol == pyglet.window.key.RIGHT:
        movement_direction = 1
    if symbol == pyglet.window.key.SPACE:
        if len(shooting_lines) < 1:
            shooting_lines.append(pyglet.shapes.Line(spaceship_sprite.x, spaceship_sprite.y+50, spaceship_sprite.x, spaceship_sprite.y+100, color=(255, 0, 0), width=2))

def update_enemies(dt):
    global enemy_movement_direction, enemy_speed 
    for enemy in enemies_sprites:
        enemy.x += enemy_movement_direction * enemy_speed * dt
        # Change direction when the enemy reaches the edge of the window
        if enemy.x > game_window.width or enemy.x < 0:
            enemy_movement_direction *= -1


def update_speed_and_position(dt):
    global enemy_speed, enemy_movement_direction
    enemy_speed += 0.1
    for enemy in enemies_sprites:
        enemy.y -= 10
        enemy.x += enemy_movement_direction * enemy_speed * dt



def on_draw(dt):
    global spaceship_sprite,shooting_lines,enemy_movement_direction, enemies_sprites,game_over_label,you_won_label
    # Clear the window
    game_window.clear()
    if len(enemies_sprites) == 0:
        you_won_label = True
        game_window.pop_handlers()
        you_won_label.visible = True
        game_over_label.visible = False
    else:
        spaceship_sprite.x += movement_direction * 200 * dt
        spaceship_sprite.x = max(150, min(game_window.width - spaceship_sprite.width - 250, spaceship_sprite.x))
        stars_sprite.draw()
        spaceship_sprite.draw()
        for line in shooting_lines:
            line.draw()

        for enemy in enemies_sprites:
            try:
                if ((shooting_lines[0].x > (enemy.x - 25)) and (shooting_lines[0].x < (enemy.x + 25))) and (shooting_lines[0].y2 < enemy.y + 25 and shooting_lines[0].y2 > enemy.y - 25):              
                    enemies_sprites.remove(enemy)
                    shooting_lines.pop(0)
            except:
                pass
        if (enemies_sprites[0].x > game_window.width - enemies_sprites[0].width - 750) or (enemies_sprites[(len(enemies_sprites) - 1)].x < 350):
            enemy_movement_direction *= -1
        for enemy in enemies_sprites:
            enemy.x += enemy_movement_direction * 50 * dt 
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()


        # pyglet.app.exit()
    if game_over:
        game_over_label.draw()  
        # pyglet.app.exit()
        # game_over_label

def update(dt):
    for line in shooting_lines:
        # line.y1 += 10
        line.y2 += 10
        line.y += 10
        if line.y2 >= game_window.height:
            shooting_lines.remove(line)
    for bullet in enemy_bullets:
        bullet.y -= 200 * dt
        if bullet.y < 0:
            enemy_bullets.remove(bullet)
    if game_over_label.visible:
        game_over_label.draw()


# Create the game window
game_window = pyglet.window.Window(caption="Space Invaders")
game_window.set_fullscreen(True)
game_over_label = pyglet.text.Label("Game Over", x=game_window.width//2, y=game_window.height//2, anchor_x='center', anchor_y='center', color=(255, 0, 0, 255), font_size=36, bold=True)
game_over_label.visible = False
you_won_label = pyglet.text.Label("You Won!", x=game_window.width//2, y=game_window.height//2, anchor_x='center', anchor_y='center', color=(0, 255, 0, 255), font_size=36, bold=True)
game_over_label.visible = False

game_window.push_handlers(on_key_press=on_key_press)
game_window.push_handlers(on_key_press=on_key_release)
pyglet.clock.schedule_interval(on_draw, 1/60.0)
pyglet.clock.schedule_interval(update_enemies, 1/60.0)
pyglet.clock.schedule_interval(update_speed_and_position, 20)
pyglet.clock.schedule_interval(fire_bullets, 1)
pyglet.clock.schedule_interval(check_collision, 1/60)
print(game_window.height)
print(game_window.width)
stars_gif = pyglet.image.load_animation('ccc.gif')

stars_sprite = pyglet.sprite.Sprite(stars_gif)
stars_sprite.x = 0
stars_sprite.y = 0

pyglet.clock.schedule_interval(update, 1/60.0)
spaceship_image = pyglet.image.load('mig.png')
spaceship_sprite = pyglet.sprite.Sprite(spaceship_image)
spaceship_sprite.x = game_window.width / 2
spaceship_sprite.y = 50
shooting_lines = []

enemies_image = pyglet.image.load('enemy_ship.png')
enemies_sprites = []
for i in range(10):
    enemy_sprite = pyglet.sprite.Sprite(enemies_image)
    enemy_sprite.x = i*50 # this will give them different x positions
    enemy_sprite.y = game_window.height - 150
    enemies_sprites.append(enemy_sprite)
    



# Run the game
pyglet.app.run()
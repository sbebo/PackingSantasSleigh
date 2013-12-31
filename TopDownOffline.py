"""
Packing Santa's Sleigh -- Sample Submission
Approach: 
- Sort presents in correct order so that smallest PresentId gets packed first.
- Start packing the sleigh at (1000,1000,1). Pack along y=1000, z=1 until full
- Move y to min_occupied_y. Pack until full.
- When y is full, move to z = max_occupied_z.
"""

import os
import csv
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

SLEIGH_LENGTH = 1000
MAX_LAYERS = 1000
#MAX_LAYERS = 999999 
PLOT = False
WRITE = False

# Plotting
xpos, ypos, zpos, dx, dy, dz = [],[],[],[],[],[]
colors = []

class Layer:
   """ Object to keep track of present position and max extent in sleigh so far. """    
   def __init__(self, id, zbase, leftovers):
        self.id = id
        self.z_base = zbase 
        self.z_max = zbase 
        self.presents = []
        self.presents.extend(leftovers)
        self.tree = Tree()


   """ Add present to layer """
   def add_present(self, present):
      self.presents.append(present)
      self.z_max = max(self.z_max, layer.z_base + present.z_depth - 1)
      return True

   """ Pack the presents """
   def pack(self):
      self.guillotine_pack()
      return

   def max_rect_pack(self):
      rect = Rectangle() #entire shelf
      self.free_rectangles = [rect]
      self.used_rectangles = []

      sorties = int(0.7*len(self.presents))
      tmp = self.presents[:sorties]
      tmp.sort(key= lambda p : p.area, reverse=True)
      tmp.extend(self.presents[sorties:])
      self.presents = []
      leftovers = []
      full = False
      for present in tmp:
         if full == True:
            leftovers.append(present)
            continue
         
         coordinates = self.pack_present(present) 
         
         if coordinates is None:
            full = True
            leftovers.append(present)
            continue
         else:
            [x1, x2, y1, y2, z1, z2] = coordinates
            present.xpos = min(x1,x2)
            present.ypos = min(y1,y2)
            present.zpos = min(z1,z2)
            self.presents.append(present)
            self.z_max = max(self.z_max, present.zpos + present.z_depth - 1)
#      print [p.id for p in leftovers]
      self.presents.sort(key= lambda p : p.id)
      leftovers.sort(key= lambda p : p.id)
      return leftovers


   def pack_present(self, present):
      #find the new rectangle where to store the present
      newRect = self.find_position()
      if newRect = None:
         return None
     
      #detect which rectangles are affected by splitting the new rectangle
      toDelete= []
      for i,r in enumerate(self.free_rectangles):
         if self.split_rect(r, newRect):
            toDelete.append(i)
      for i in toDelete:
         del self.free_rectangles[i]
      
      # prune the list 
      self.prune_free()

      used_rectangles.append(newRect)
      
      return newRect


   def find_position(self, present):
      bestRect = Rectangle()
      bestShortSideFit = SLEIGH_LENGTH 
      bestLongSideFit = SLEIGH_LENGTH 
      for i,r in enumerate(self.free_rectangles):

         ####################
         if r.width >= present.width and r.height >= present.height:
            leftoverHoriz = r.width - present.width
            leftoverVert = r.height - present.height
            shortSideFit = min(leftoverHoriz, leftoverVert)
            longSideFit = max(leftoverHoriz, leftoverVert)

            if shortSideFit < bestShortSideFit or (shortSideFit == bestShortSideFit and longSideFit < bestLongSideFit):
               bestRect.xpos = r.xpos
               bestRect.ypos = r.ypos
               bestRect.width = present.width
               bestRect.height = present.height
               bestShortSideFit = shortSideFit
               bestLongSideFit = longSideFit

         ####################
         if r.width >= present.height and r.height >= present.height:
            present.rotate()
            leftoverHoriz = r.width - present.width
            leftoverVert = r.height - present.height
            shortSideFit = min(leftoverHoriz, leftoverVert)
            longSideFit = max(leftoverHoriz, leftoverVert)

            if shortSideFit < bestShortSideFit or (shortSideFit == bestShortSideFit and longSideFit < bestLongSideFit):
               bestRect.xpos = r.xpos
               bestRect.ypos = r.ypos
               bestRect.width = present.width
               bestRect.height = present.height
               bestShortSideFit = shortSideFit
               bestLongSideFit = longSideFit
            else:
               present.rotate()
      
      if bestShortSideFit == SLEIGH_LENGTH:
         return None
      return bestRect

   def split_rect(self, freeRect, usedRect):
      #TODO: check bounds!!!
      if not freeRect.overlap(usedRect):
         return False
 
      if (usedRect.xpos <= freeRect.xpos + freeRect.width-1 and usedRect.xpos + usedRect.width-1 >= freeRect.xpos):
        
              # New node at the top side of the used node.
              if (usedRect.ypos > freeRect.ypos and usedRect.ypos < freeRect.ypos + freeRect.height-1):
                 #horrible
                 newRect = Rectangle()
                 newRect.xpos = freeRect.xpos
                 newRect.ypos = freeRect.ypos
                 newRect.width = freeRect.width
                 newRect.height = freeRect.height
                 
                 newRect.height = usedRect.ypos - newRect.ypos
                 self.free_rectangles.append(newRect)

              # New node at the bottom side of the used node.
              if (usedRect.ypos + usedRect.height < freeRect.ypos + freeRect.height):
                 #horrible
                 newRect = Rectangle()
                 newRect.xpos = freeRect.xpos
                 newRect.ypos = freeRect.ypos
                 newRect.width = freeRect.width
                 newRect.height = freeRect.height
             
                 newRect.ypos = usedRect.ypos + usedRect.height
                 newRect.height = freeRect.ypos + freeRect.height - (usedRect.ypos + usedRect.height)
                 self.free_rectangles.append(newRect)

        if (usedRect.ypos < freeRect.ypos + freeRect.height and usedRect.ypos + usedRect.height > freeRect.ypos):
        
              # New node at the left side of the used node.
              if (usedRect.xpos > freeRect.xpos and usedRect.xpos < freeRect.xpos + freeRect.width):
                 #horrible
                 newRect = Rectangle()
                 newRect.xpos = freeRect.xpos
                 newRect.ypos = freeRect.ypos
                 newRect.width = freeRect.width
                 newRect.height = freeRect.height
             
                 newRect.width = usedRect.xpos - newRect.xpos
                 self.free_rectangles.append(newRect)

              # New node at the right side of the used node.
              if (usedRect.xpos + usedRect.width < freeRect.xpos + freeRect.width):
                 #horrible
                 newRect = Rectangle()
                 newRect.xpos = freeRect.xpos
                 newRect.ypos = freeRect.ypos
                 newRect.width = freeRect.width
                 newRect.height = freeRect.height
            
                 newRect.xpos = usedRect.xpos + usedRect.width
                 newRect.width = freeRect.xpos + freeRect.width - (usedRect.xpos + usedRect.width)
                 self.free_rectangles.append(newRect)

        return True


   def prune_free(self):
      toDelete = set()
      for i,r in enumerate(self.free_rectangles):
         for j,r2 in enumerate(self.free_rectangles):
            if j>i:
               if r2.contains(r):
                  toDelete.add(r)
                  break
               if r.contains(r2):
                  toDelete.add(r2)
      for i in toDelete:
         del self.free_rectangles[i]

      return


   """ Guillotine packing """
   def guillotine_pack(self):
#      print len(self.presents)
      sorties = int(0.7*len(self.presents))
      tmp = self.presents[:sorties]
      tmp.sort(key= lambda p : p.area, reverse=True)
      tmp.extend(self.presents[sorties:])
      self.presents = []
      leftovers = []
      full = False
      for present in tmp:
         if full == True:
            leftovers.append(present)
            continue
         
         coordinates = self.guillotine_pack_present(present) 
         
         if coordinates is None:
            full = True
#            print "First leftover", present.id
            leftovers.append(present)
            continue
         else:
            [x1, x2, y1, y2, z1, z2] = coordinates
            present.xpos = min(x1,x2)
            present.ypos = min(y1,y2)
            present.zpos = min(z1,z2)
            self.presents.append(present)
            self.z_max = max(self.z_max, present.zpos + present.z_depth - 1)
#      print [p.id for p in leftovers]
      self.presents.sort(key= lambda p : p.id)
      leftovers.sort(key= lambda p : p.id)
      return leftovers

   """ Try to pack a present in this layer """ #TODO better packing!
   def guillotine_pack_present(self, present):
      leaf = self.tree.root.insert(present)
      #print tree
      if leaf is None:
         present.rotate()
         leaf = self.tree.root.insert(present)

      if leaf is None:
         # Really no space! Rotate it back
         present.rotate()
         return None
         #open a new layer!
         #layer.z_base = layer.z_max + 1
         #tree.root = Node()
         #leaf = tree.root.insert(present)

      x1 = leaf.xpos
      x2 = leaf.xpos - leaf.width + 1
      y1 = leaf.ypos
      y2 = leaf.ypos - leaf.height + 1 
      z1 = layer.z_base 
      z2 = z1 + present.z_depth - 1

      return [x1, x2, y1, y2, z1, z2]

   
   
   """ Copy presents and sort them decreasingly by tallest z-point they reach (if no compactor, the z_pos term is all the same (z_base), but otherwise it's not). """
   def sort_presents(self):
      self.sorted_presents = list(self.presents)
      self.sorted_presents.sort(key= lambda p : (p.zpos+p.z_depth-1), reverse=True)
      return self.sorted_presents
     
   """ Compactor """
   def compact(self, prev_layer):
      #prev_layer.z_base # do not exceed
      #print "Layer", self.id
      z_min = prev_layer.z_base-1 #z_min up to current present. then, following presents must not be smaller, they can be equal or greater.

      # recompute z_max
      self.z_max = self.z_base
      
      for p in self.presents: #in order of id!
         # presents in the previous layer sorted by decreasing z-height
         for up_p in prev_layer.sort_presents():
            if p.overlap(up_p):
               # this is the tallest overlapping present: you can move down the present, if possible. 
               # if not possible, break!
               diff = p.zpos - (up_p.zpos+up_p.z_depth)
               if diff > 0 and (p.zpos - diff) >= z_min:
#                  print "good overlap", p.id, diff
#                  print "previous pos", p.zpos
                  p.zpos -= diff
#                  print "new pos", p.zpos
                  z_min = max(p.zpos, z_min)
               break
         z_min = max(p.zpos, z_min)
         #print "zmin", z_min
         self.z_max = max(self.z_max, p.zpos + p.z_depth - 1)
      
      return


   """ Finalize shelf """
   def finalize_shelf(self):
      #fracs = offset.astype(float)/offset.max()
      #norm = colors.normalize(fracs.min(), fracs.max())
      for i,p in enumerate(self.presents):
         if self.id <= MAX_LAYERS:
            x1, x2, y1, y2, z1, z2 = p.xpos, p.xpos+p.width-1, p.ypos, p.ypos + p.height-1, p.zpos, p.zpos + p.z_depth-1
            xpos.append(min(x1,x2))
            ypos.append(min(y1,y2))
            zpos.append(min(z1,z2))
            dx.append(abs(x1-x2))
            dy.append(abs(y1-y2))
            dz.append(abs(z1-z2))
            colors.append(cm.jet(float(i)/len(self.presents)))

   """ Reflect x and y axis """ 
   def reflect_shelf(self):
      #print "Flipping layer", self.id
      for p in self.presents:
         p.xpos = 1 + SLEIGH_LENGTH - (p.xpos + p.width - 1)
         p.ypos = 1 + SLEIGH_LENGTH - (p.ypos + p.height - 1)
         


   """ Write next line """
   def write_shelf(self, writer, maxz):
      for p in self.presents:
         x1, x2, y1, y2, z1, z2 = p.xpos, p.xpos+p.width-1, p.ypos, p.ypos + p.height-1, p.zpos, p.zpos + p.z_depth-1
         z1 = maxz - z1 + 1
         z2 = maxz - z2 + 1

         list_vertices = [x1, y1, z1]
         list_vertices += [x1, y2, z1]
         list_vertices += [x2, y1, z1]
         list_vertices += [x2, y2, z1]
         list_vertices += [x1, y1, z2]
         list_vertices += [x1, y2, z2]
         list_vertices += [x2, y1, z2]
         list_vertices += [x2, y2, z2]
         writer.writerow([p.id] + list_vertices)
      return 

class Tree:
   def __init__(self):
      self.root = Node()

class Rectangle:
   def __init__(self, w=SLEIGH_LENGTH, h=SLEIGH_LENGTH):
      self.xpos = 1 
      selx.ypos = 1
      self.width = w 
      self.height = h 
 
   def overlap(self, rectangle):
      # make sure that positions are good, not 0's!

      if (self.xpos+self.width-1) < rectangle.xpos:
         return False
      if self.xpos > (rectangle.xpos+rectangle.width-1):
         return False
      if (self.ypos+self.height-1) < rectangle.ypos:
         return False
      if self.ypos > (rectangle.ypos+rectangle.height-1): 
         return False
      return True

class Present:
   def __init__(self, row):
      self.id = int(row[0])
      dim = [int(x) for x in row[1:]]
      dim.sort()
      self.width = dim[0]     # along x-axis 
      self.height = dim[1]    # along y-axis
      self.z_depth = dim[2]   # along z-axis
      self.area = self.width * self.height
      self.xpos = 0
      self.ypos = 0
      self.zpos = 0
  
   # rotate on the x-y plane
   def rotate(self):
      self.width, self.height = self.height, self.width
      # should also change positions? it's not univocal.

   def overlap(self, present):
      # make sure that positions are good, not 0's!

      if (self.xpos+self.width-1) < present.xpos:
         return False
      if self.xpos > (present.xpos+present.width-1):
         return False
      if (self.ypos+self.height-1) < present.ypos:
         return False
      if self.ypos > (present.ypos+present.height-1): 
         return False
      return True
      

class Node:
   def __init__(self):
      self.child = [None, None]
      self.xpos = SLEIGH_LENGTH 
      self.ypos = SLEIGH_LENGTH 
      self.width = SLEIGH_LENGTH 
      self.height = SLEIGH_LENGTH 
      self.id = None

   def insert(self, present):
      # if not leaf, DFS leftmost child
      if self.child[0] is not None and self.child[1] is not None:
         newNode = self.child[0].insert(present)
         if newNode is not None:
            return newNode
         return self.child[1].insert(present)
      
      # if it's a leaf
      else:
         # if the space is occupied
         if self.id is not None:
            return None
        
         # if the space is too small
#         if self.width < present.width or self.height < present.height:
#            present.rotate()
         if self.width < present.width or self.height < present.height:
#            present.rotate() #rotate it back
            return None

         # if the space is perfect
         if self.width == present.width and self.height == present.height:
            self.id = present.id
            return self

         # if the space is larger,
         # split the space 
         self.child[0] = Node()
         self.child[1] = Node()

         dw = self.width - present.width
         dh = self.height - present.height

         # cut vertically 
         if dw > dh:
            self.child[0].xpos = self.xpos
            self.child[0].ypos = self.ypos
            self.child[0].width = present.width
            self.child[0].height = self.height
            
            self.child[1].xpos = self.xpos - present.width
            self.child[1].ypos = self.ypos
            self.child[1].width = self.width - present.width
            self.child[1].height = self.height
         # cut horizontally
         else:
            self.child[0].xpos = self.xpos
            self.child[0].ypos = self.ypos
            self.child[0].width = self.width 
            self.child[0].height = present.height
            
            self.child[1].xpos = self.xpos
            self.child[1].ypos = self.ypos - present.height
            self.child[1].width = self.width 
            self.child[1].height = self.height - present.height

         # insert in first child
         return self.child[0].insert(present)




if __name__ == "__main__":
    
   path = '.'
   presentsFilename = os.path.join(path, 'presents.csv')
   submissionFilename = os.path.join(path, 'test.csv')
   
   # create header for submission file: PresentId, x1,y1,z1, ... x8,y8,z8
   header = ['PresentId']
   for i in xrange(1,9):
       header += ['x' + str(i), 'y' + str(i), 'z' + str(i)]
    
   layer = Layer(1,1,[])
   prev_layer = None
   maxz = 1
   with open(presentsFilename, 'rb') as f:
      f.readline() # header
      fcsv = csv.reader(f)
      cumul_area = 0
      for row in fcsv:
         if int(row[0])%10000 == 0:
           print row[0]

         present = Present(row)
         
         added_present = False
         if cumul_area + present.area < SLEIGH_LENGTH*SLEIGH_LENGTH:
            cumul_area += present.area
            added_present = layer.add_present(present) 
         
         if not added_present:
#            print "Full layer!"
            # area is full! try to pack! return presents that do not fit
            leftovers = layer.pack()
#            print "Leftovers",len(leftovers)
#            print sum(p.area for p in layer.presents)/float(SLEIGH_LENGTH*SLEIGH_LENGTH)
            #print layer.id, present.id, float(present.id)/layer.id
            if layer.id % 2 == 0:
               layer.reflect_shelf()
            
            # compact shelf down (if possible), preserving order
            if prev_layer is not None:
               layer.compact(prev_layer)
            
            # store coordinates for plotting
            if PLOT:
               layer.finalize_shelf()
            
            # open new shelf and add current present
            cumul_area = sum(p.area for p in leftovers)
            prev_layer = layer
            if layer.id >= MAX_LAYERS:
               break
            layer = Layer(prev_layer.id+1, prev_layer.z_max+1, leftovers)
            added_present = layer.add_present(present)

         if not added_present:
            print "Something wrong"

   maxz = layer.z_max

   print "Max z =", maxz

   if PLOT:
      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
      ax.bar3d(xpos,ypos,zpos,dx,dy,dz,color=colors)
      #ax.bar3d(xpos,ypos,zpos,dx,dy,dz,color='r')
      ax.set_xlim3d(0, 1000)
      ax.set_ylim3d(0, 1000)
      print "Plotting"
      plt.show()

   if WRITE:
      print "Writing file"
      layer = Layer(1,1,[])
      prev_layer = None
      with open(presentsFilename, 'rb') as f:
         with open(submissionFilename, 'wb') as w:
            f.readline() # header
            fcsv = csv.reader(f)
            wcsv = csv.writer(w)
            wcsv.writerow(header)
            
            cumul_area = 0
            for row in fcsv:
               if int(row[0])%10000 == 0:
                 print row[0]

               present = Present(row)
               
               added_present = False
               if cumul_area + present.area < SLEIGH_LENGTH*SLEIGH_LENGTH:
                  cumul_area += present.area
                  added_present = layer.add_present(present) 
               
               if not added_present:
                  leftovers = layer.pack()

                  #print layer.id, present.id, float(present.id)/layer.id
                  if layer.id % 2 == 0:
                     layer.reflect_shelf()

                  # compact shelf down (if possible), preserving order 
                  if prev_layer is not None:
                     layer.compact(prev_layer)
                  
                  # write to file
                  layer.write_shelf(wcsv, maxz)
                  
                  # open new shelf and add current present
                  cumul_area = sum(p.area for p in leftovers)
                  prev_layer = layer
                  if layer.id >= MAX_LAYERS:
                     break
                  layer = Layer(prev_layer.id+1, prev_layer.z_max+1, leftovers)
                  added_present = layer.add_present(present)

               if not added_present:
                  print "Something wrong"
            
            if added_present == True:
               # rows are over. 
               # last layer was not "full" (area-wise), so it has not been packed yet!
               leftovers = layer.pack()
               layer.write_shelf(wcsv,maxz)
               #however, it can still have leftovers
               if len(leftovers)>0: 
                  prev_layer = layer
                  layer = Layer(prev_layer.id+1, prev_layer.z_max+1, leftovers)
                  layer.write_shelf(wcsv,maxz)


   print 'Done'

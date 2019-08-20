import vtk

# Visualize
colors = vtk.vtkNamedColors()
# Create points
p0 = [0.0, 0.0, 0.0]
p1 = [0.0, 1.0, 0.0]
p2 = [1.0, 0.0, 0.0]
p3 = [1.0, 1.0, 0.0]


# LineSource:画两个点的线
def createLine1():
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(p0)
    lineSource.SetPoint2(p1)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    return mapper


# LineSource 多点连续直线
def createLine2():
    lineSource = vtk.vtkLineSource()
    points = vtk.vtkPoints()
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p1)
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p3)
    lineSource.SetPoints(points)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    return mapper


# LineSource 多点设置几何结构+拓扑结构
def createLine3():
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p1)
    points.InsertNextPoint(p2)
    points.InsertNextPoint(p3)

    # Create a cell array to store the lines in and add the lines to it
    lines = vtk.vtkCellArray()

    # for i in range(0, 3, 2):
    #     line = vtk.vtkLine()
    #     line.GetPointIds().SetId(0, i)
    #     line.GetPointIds().SetId(1, i + 1)
    #     lines.InsertNextCell(line)
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)
    lines.InsertNextCell(line)
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 2)
    lines.InsertNextCell(line)
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 3)
    lines.InsertNextCell(line)

    # Create a polydata to store everything in
    linesPolyData = vtk.vtkPolyData()

    # Add the points to the dataset         几何结构
    linesPolyData.SetPoints(points)

    # Add the lines to the dataset          拓扑结构
    linesPolyData.SetLines(lines)

    # Setup actor and mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)
    return mapper


def main():
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Line")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualize
    colors = vtk.vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("Silver"))

    actor = vtk.vtkActor()
    # 第一种方式
    # actor.SetMapper(createLine1())
    # 第二种方式
    # actor.SetMapper(createLine2())
    # 第三种方式
    actor.SetMapper(createLine3())

    actor.GetProperty().SetLineWidth(1)
    actor.GetProperty().SetOpacity(.5)
    actor.GetProperty().SetColor(colors.GetColor3d("Peacock"))
    renderer.AddActor(actor)

    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()